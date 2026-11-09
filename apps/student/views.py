import os
import io
import zipfile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count, Q

from apps.courses.models import Course, Lesson
from apps.learning.models import Enrollment, LessonProgress, Assignment, AssignmentSubmission, SubmissionStatus
from apps.projects.models import (
    Project, ProjectLike, ProjectStatus, ProjectType,
    ProjectLanguage, ProjectMode, ProjectFile
)
from apps.projects.forms import ProjectCreateForm, ProjectSubmissionForm
from .services import (
    get_student_overview_stats,
)


# ==============================================================================
# 1. BOSH SAHIFA, DASHBOARD, BIZ HAQIMIZDA
# ==============================================================================

@login_required
def student_home_view(request):
    """Bosh sahifa: platformaning asosiy oynasi (sidebar saqlanadi)."""
    from apps.blog.models import Post
    enrolled_ids = Enrollment.objects.filter(user=request.user).values_list('course_id', flat=True)
    courses = Course.objects.filter(is_published=True).exclude(id__in=enrolled_ids).select_related('category')[:6]
    posts = Post.objects.filter(is_published=True).select_related('category')[:3]
    return render(request, 'student/home.html', {
        'courses': courses, 'posts': posts, 'active_menu': 'home',
        'platform_courses': Course.objects.filter(is_published=True).count(),
    })


@login_required
def student_dashboard_view(request):
    """Dashboard: hozir o'qilayotgan kurslar va natijalar."""
    stats = get_student_overview_stats(request.user)
    enrollments = [e for e in stats['enrollments'] if not e.completed_at and e.progress_percent < 100]
    recent_submissions = AssignmentSubmission.objects.filter(
        student=request.user
    ).select_related('assignment__lesson__module__course').order_by('-updated_at')[:5]
    return render(request, 'student/dashboard.html', {
        'stats': stats, 'enrollments': enrollments,
        'recent_submissions': recent_submissions, 'active_menu': 'dashboard',
    })


@login_required
def student_about_view(request):
    """Biz haqimizda: platforma, aloqa, maxfiylik va foydalanish shartlari."""
    return render(request, 'student/about.html', {'active_menu': 'about'})


# ==============================================================================
# 2. VAZIFALAR LABORATORIYASI (ASSIGNMENT STUDIO)
# ==============================================================================

@login_required
def student_assignments_hub_view(request):
    """Barcha kurslar bo'yicha amaliy vazifalar markazi va filtri."""
    status_filter = request.GET.get('status', 'all').strip()
    course_filter = request.GET.get('course', '').strip()

    # O'quvchi yozilgan kurslar
    user_courses = Course.objects.filter(enrollments__user=request.user)

    # Barcha amaliy vazifalar
    assignments_qs = Assignment.objects.filter(
        lesson__module__course__in=user_courses,
        is_active=True
    ).select_related('lesson__module__course')

    if course_filter.isdigit():
        assignments_qs = assignments_qs.filter(lesson__module__course_id=int(course_filter))

    # O'quvchining yuborilgan yechimlari xaritasi
    submissions_map = {
        sub.assignment_id: sub
        for sub in AssignmentSubmission.objects.filter(student=request.user)
    }

    # Vazifalarni statusi bilan biriktirish
    items = []
    for assign in assignments_qs:
        sub = submissions_map.get(assign.id)
        current_status = sub.status if sub else 'unsubmitted'

        if status_filter != 'all' and current_status != status_filter:
            continue

        items.append({
            'assignment': assign,
            'submission': sub,
            'status': current_status,
        })

    # Statistika hisobi
    all_assign_count = assignments_qs.count()
    approved_count = sum(1 for s in submissions_map.values() if s.status == SubmissionStatus.APPROVED)
    pending_count = sum(1 for s in submissions_map.values() if s.status == SubmissionStatus.PENDING)
    rejected_count = sum(1 for s in submissions_map.values() if s.status == SubmissionStatus.REJECTED)
    unsubmitted_count = all_assign_count - len(submissions_map)

    context = {
        'items': items,
        'user_courses': user_courses,
        'status_filter': status_filter,
        'course_filter': course_filter,
        'all_assign_count': all_assign_count,
        'approved_count': approved_count,
        'pending_count': pending_count,
        'rejected_count': rejected_count,
        'unsubmitted_count': max(0, unsubmitted_count),
        'active_menu': 'assignments',
    }
    return render(request, 'student/assignments_hub.html', context)


@login_required
def student_assignment_solve_view(request, assignment_id):
    """
    Platformaning o'zida vazifani bajarish studiyasi:
    Split-screen, kod muharriri (Monaco/Ace), shablon kod, blok-sxema va o'qituvchiga yuborish.
    """
    assignment = get_object_or_404(
        Assignment.objects.select_related('lesson__module__course'),
        id=assignment_id,
        is_active=True
    )
    course = assignment.lesson.module.course

    # Kursga a'zolikni tekshirish
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    if not is_enrolled and not (request.user.is_staff or request.user.role in ['instructor', 'admin']):
        messages.error(request, "Vazifani bajarish uchun avval ushbu kursga yozilishingiz lozim.")
        return redirect('course_detail', slug=course.slug)

    submission = AssignmentSubmission.objects.filter(assignment=assignment, student=request.user).first()

    if request.method == 'POST':
        # Qabul qilingan vazifani qayta yuborishni bloklash
        if submission and submission.status == SubmissionStatus.APPROVED:
            messages.info(request, "Ushbu vazifangiz allaqachon muvaffaqiyatli qabul qilingan.")
            return redirect('student_assignment_solve', assignment_id=assignment.id)

        submitted_code = request.POST.get('submitted_code', '').strip()
        flowchart_data = request.POST.get('flowchart_data', '').strip()
        attached_file = request.FILES.get('attached_file')

        if attached_file:
            max_size = 25 * 1024 * 1024  # 25 MB
            allowed_extensions = {'.zip', '.rar', '.pdf', '.dart', '.py', '.sql', '.txt', '.docx', '.png', '.jpg'}
            ext = os.path.splitext(attached_file.name)[1].lower()
            if attached_file.size > max_size or ext not in allowed_extensions:
                messages.error(request, "Fayl hajmi 25 MB dan kichik va ruxsat etilgan formatda (.zip, .dart, .py, .pdf) bo'lishi kerak.")
                return redirect('student_assignment_solve', assignment_id=assignment.id)

        if not submitted_code and not flowchart_data and not attached_file:
            messages.error(request, "Iltimos, kod yozing, blok-sxema chizing yoki fayl yuklang.")
            return redirect('student_assignment_solve', assignment_id=assignment.id)

        if not submission:
            submission = AssignmentSubmission(
                assignment=assignment,
                student=request.user,
                submitted_code=submitted_code,
                flowchart_data=flowchart_data,
                attached_file=attached_file,
                status=SubmissionStatus.PENDING,
            )
        else:
            if submitted_code:
                submission.submitted_code = submitted_code
            if flowchart_data:
                submission.flowchart_data = flowchart_data
            if attached_file:
                submission.attached_file = attached_file
            submission.status = SubmissionStatus.PENDING
            submission.instructor_feedback = ""

        submission.save()
        messages.success(request, "Vazifangiz o'qituvchiga muvaffaqiyatli yuborildi! Tekshirilgach sizga xabar beriladi.")
        return redirect('student_assignment_solve', assignment_id=assignment.id)

    context = {
        'assignment': assignment,
        'course': course,
        'submission': submission,
        'active_menu': 'assignments',
    }
    return render(request, 'student/assignment_solve.html', context)


# ==============================================================================
# 3. LOYIHALAR BO'LIMI (PROJECTS & IN-BROWSER IDE)
# ==============================================================================

# Talaba kodi web-server jarayonida HECH QACHON exec() qilinmaydi: barcha bajarish
# apps.core.code_runner orqali alohida, resurslari cheklangan sandbox'ga yuboriladi.
# Hozircha faqat Python qo'llab-quvvatlanadi; boshqa tillar uchun soxta natija
# ko'rsatilmaydi — halol "qo'llab-quvvatlanmaydi" xabari qaytariladi.
DEFAULT_PROJECT_STDIN = ""


def _format_run_output(res):
    """RunResult'ni terminal uchun matnga aylantiradi."""
    parts = []
    if res.stdout:
        parts.append(res.stdout.rstrip('\n'))
    if res.stderr:
        parts.append(res.stderr.rstrip('\n'))
    if res.friendly_error:
        parts.append(f"[Izoh] {res.friendly_error}")
    if res.status == 'ok' and not res.stdout and not res.stderr:
        parts.append("[Dastur muvaffaqiyatli yakunlandi, ekranga hech narsa chiqarilmadi.]")
    if res.status in ('unavailable', 'busy', 'invalid') and not res.stderr:
        parts.append("[Kod bajarish xizmati vaqtincha mavjud emas.]")
    return "\n".join(parts)


def _execute_code_safely(language, code, files=None, entry='main.py', stdin=None):
    """
    Kodni izolyatsiyalangan sandbox'da bajaradi.

    Qaytaradi: (terminal_matni, muvaffaqiyatli_mi, elapsed_ms)
    """
    from apps.core.code_runner import run_python

    if language != 'python':
        return (
            f"[{language.upper()}] Bu til uchun brauzerda kodni bajarish hozircha qo'llab-quvvatlanmaydi. "
            "Kodingiz saqlanadi; uni o'z kompyuteringizda ishga tushirib ko'ring.",
            False,
            0,
        )
    res = run_python(code if files is None else None, files=files, entry=entry,
                     stdin=DEFAULT_PROJECT_STDIN if stdin is None else stdin)
    return _format_run_output(res), res.ok, res.elapsed_ms


@login_required
def student_projects_view(request):
    """Loyihalar vitrinasi: Mening loyihalarim, Bitiruv loyihalari va Showcase."""
    tab = request.GET.get('tab', 'my').strip()

    my_projects = Project.objects.filter(
        author=request.user
    ).prefetch_related('files').order_by('-created_at')

    # Showcase loyihalari (barcha tasdiqlangan va sara loyihalar)
    showcase_projects = Project.objects.filter(
        status__in=[ProjectStatus.APPROVED, ProjectStatus.FEATURED]
    ).select_related('author__profile', 'course').order_by('-likes_count', '-created_at')

    # Foydalanuvchi layk bosgan loyihalar IDlari
    user_liked_ids = set(
        ProjectLike.objects.filter(user=request.user).values_list('project_id', flat=True)
    )

    # Kurs bitiruv loyihalari (Capstone takliflari)
    capstone_projects = Project.objects.filter(
        project_type=ProjectType.CAPSTONE,
        status__in=[ProjectStatus.APPROVED, ProjectStatus.FEATURED]
    ).select_related('author__profile', 'course')

    context = {
        'tab': tab,
        'my_projects': my_projects,
        'showcase_projects': showcase_projects,
        'capstone_projects': capstone_projects,
        'user_liked_ids': user_liked_ids,
        'active_menu': 'projects',
    }
    return render(request, 'student/projects_list.html', context)


@login_required
def student_project_create_view(request):
    """
    Yangi loyiha qo'shish:
    Foydalanuvchidan faqat Loyiha nomi, Dasturlash tili va Loyiha tuzilishi (Ko'p faylli yoki Konsol) so'raladi.
    Yaratilgach, avtomatik ravishda IDE muhitiga yo'naltiriladi!
    """
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.status = ProjectStatus.DRAFT
            if not project.tagline:
                project.tagline = f"{project.get_language_display()} tilidagi {project.get_project_mode_display().lower()}"
            project.save()

            # Boshlang'ich fayllarni avtomatik yaratish
            project.create_default_files()

            messages.success(request, f"«{project.title}» loyihasi yaratildi! Kod yozishni boshlashingiz mumkin.")
            return redirect('student_project_ide', project_id=project.id)
    else:
        form = ProjectCreateForm()

    user_courses = Course.objects.filter(enrollments__user=request.user)
    context = {
        'form': form,
        'user_courses': user_courses,
        'active_menu': 'projects',
    }
    return render(request, 'student/project_create.html', context)


@login_required
def student_project_ide_view(request, project_id):
    """
    Loyihaning asosiy In-Browser IDE oynasi:
    - Ko'p faylli rejimda: Chapda fayllar daraxti (yangi fayl/papka), o'ngda kod muharriri (Ace Editor), pastda terminal.
    - Konsol rejimida: O'rtada blok-sxema (Mermaid avtomatik generatsiya), o'ngda kod muharriri, pastda konsol.
    """
    project = get_object_or_404(Project, id=project_id)
    if project.author != request.user and not request.user.is_staff:
        messages.error(request, "Siz faqat o'zingizning loyihalaringizni tahrirlashingiz mumkin.")
        return redirect('student_projects')

    # Agar fayllar yo'q bo'lsa boshlang'ichlarini yaratamiz
    if not project.files.exists():
        project.create_default_files()

    file_id = request.GET.get('file')
    active_file = None
    if file_id and file_id.isdigit():
        active_file = project.files.filter(id=int(file_id), is_folder=False).first()

    if not active_file:
        active_file = project.files.filter(is_folder=False).first()

    all_files = project.files.select_related('parent').order_by('-is_folder', 'name')

    context = {
        'project': project,
        'active_file': active_file,
        'files': all_files,
        'active_menu': 'projects',
    }
    return render(request, 'student/project_ide.html', context)


@login_required
def student_project_file_get_view(request, project_id, file_id):
    """Fayl ma'lumotlarini va matnini olish (AJAX)."""
    project = get_object_or_404(Project, id=project_id)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': "Ruxsat etilmagan"}, status=403)

    file_obj = get_object_or_404(ProjectFile, id=file_id, project=project)
    return JsonResponse({
        'success': True,
        'id': file_obj.id,
        'name': file_obj.name,
        'is_folder': file_obj.is_folder,
        'content': file_obj.content,
        'path': file_obj.get_full_path(),
        'extension': file_obj.extension,
    })


@login_required
@require_POST
def student_project_file_save_view(request, project_id, file_id):
    """Fayl kodini saqlash (AJAX)."""
    project = get_object_or_404(Project, id=project_id)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': "Ruxsat etilmagan"}, status=403)

    file_obj = get_object_or_404(ProjectFile, id=file_id, project=project)
    if file_obj.is_folder:
        return JsonResponse({'success': False, 'error': "Papka matniga saqlash mumkin emas"}, status=400)

    content = request.POST.get('content', '')
    file_obj.content = content
    file_obj.save(update_fields=['content', 'updated_at'])

    return JsonResponse({
        'success': True,
        'file_id': file_obj.id,
        'updated_at': file_obj.updated_at.strftime('%H:%M:%S'),
    })


@login_required
@require_POST
def student_project_file_create_view(request, project_id):
    """Loyihada yangi fayl yoki papka yaratish (AJAX)."""
    project = get_object_or_404(Project, id=project_id)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': "Ruxsat etilmagan"}, status=403)

    name = request.POST.get('name', '').strip()
    is_folder = request.POST.get('is_folder', 'false').lower() in ['true', '1']
    parent_id = request.POST.get('parent_id')

    if not name:
        return JsonResponse({'success': False, 'error': "Nom bo'sh bo'lishi mumkin emas"}, status=400)

    # Xavfsizlik: fayl nomida taqiqlangan belgilar
    if any(char in name for char in ['\\', ':', '*', '?', '"', '<', '>', '|']):
        return JsonResponse({'success': False, 'error': "Fayl nomida nojo'ya belgilar bor"}, status=400)

    parent = None
    if parent_id and parent_id.isdigit():
        parent = project.files.filter(id=int(parent_id), is_folder=True).first()

    if project.files.filter(parent=parent, name=name).exists():
        return JsonResponse({'success': False, 'error': "Bu nomli fayl yoki papka allaqachon mavjud"}, status=400)

    starter_content = ""
    if not is_folder:
        ext = name.split('.')[-1].lower() if '.' in name else ''
        if ext == 'py':
            starter_content = f"# {name}\n\ndef yangi_funksiya():\n    pass\n"
        elif ext in ['cs', 'java', 'cpp', 'js', 'dart']:
            starter_content = f"// {name}\n"
        elif ext == 'md':
            starter_content = f"# {name}\n"

    new_file = ProjectFile.objects.create(
        project=project,
        name=name,
        parent=parent,
        is_folder=is_folder,
        content=starter_content,
    )

    return JsonResponse({
        'success': True,
        'file': {
            'id': new_file.id,
            'name': new_file.name,
            'is_folder': new_file.is_folder,
            'parent_id': new_file.parent_id,
            'path': new_file.get_full_path(),
            'extension': new_file.extension,
        }
    })


@login_required
@require_POST
def student_project_file_delete_view(request, project_id, file_id):
    """Loyihadagi fayl yoki papkani o'chirish (AJAX)."""
    project = get_object_or_404(Project, id=project_id)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': "Ruxsat etilmagan"}, status=403)

    file_obj = get_object_or_404(ProjectFile, id=file_id, project=project)
    file_name = file_obj.name
    file_obj.delete()

    return JsonResponse({'success': True, 'name': file_name})


@login_required
@require_POST
def student_project_submit_view(request, project_id):
    """Loyihani ustozga tekshirish uchun topshirish."""
    project = get_object_or_404(Project, id=project_id, author=request.user)

    project.status = ProjectStatus.UNDER_REVIEW
    project.is_submitted = True
    project.submitted_at = timezone.now()
    project.save(update_fields=['status', 'is_submitted', 'submitted_at'])

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'message': "Loyihangiz ustozga ko'rib chiqish uchun muvaffaqiyatli yuborildi!",
            'status': project.status,
            'status_display': project.get_status_display(),
        })

    messages.success(request, f"«{project.title}» loyihasi ustozga tekshiruv uchun muvaffaqiyatli yuborildi!")
    return redirect('student_project_ide', project_id=project.id)


@login_required
def student_project_download_zip_view(request, project_id):
    """Loyihaning barcha fayllarini ZIP arxiv shaklida yuklab olish."""
    project = get_object_or_404(Project, id=project_id)

    # Ruxsat tekshiruvi: faqat muallif, xodimlar yoki tasdiqlangan loyihalar
    if project.author != request.user and not request.user.is_staff and project.status not in [ProjectStatus.APPROVED, ProjectStatus.FEATURED]:
        messages.error(request, "Ushbu loyiha fayllarini yuklab olish huquqiga ega emassiz.")
        return redirect('student_projects')

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        files = project.files.filter(is_folder=False)
        if not files.exists():
            zf.writestr('README.md', f'# {project.title}\n\nUshbu loyiha bo\'sh.')
        for f in files:
            zf.writestr(f.get_full_path(), f.content or '')

    zip_buffer.seek(0)
    filename = f"{project.slug or 'project'}.zip"
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
@require_POST
def student_project_delete_view(request, project_id):
    """Loyihani o'chirish."""
    project = get_object_or_404(Project, id=project_id, author=request.user)
    title = project.title
    project.delete()
    messages.success(request, f"«{title}» loyihasi butunlay o'chirildi.")
    return redirect('student_projects')


@login_required
@require_POST
def student_project_run_code_view(request, project_id):
    """Kodni ishga tushirish va terminal natijasini qaytarish (AJAX)."""
    project = get_object_or_404(Project, id=project_id)
    if project.author != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': "Ruxsat etilmagan"}, status=403)

    from apps.core.code_runner import check_rate_limit
    if not check_rate_limit(request.user.id):
        return JsonResponse({
            'success': False,
            'output': "[Cheklov] Juda ko'p ishga tushirish. Bir daqiqadan so'ng qayta urinib ko'ring.",
            'elapsed_ms': 0,
        }, status=429)

    code = request.POST.get('code', '')
    file_id = request.POST.get('file_id')
    stdin = request.POST.get('stdin', '')

    # Ko'p faylli loyiha: barcha fayllar sandbox'ga xotiradan import qilish uchun uzatiladi
    files = {}
    entry = 'main.py'
    for f in project.files.filter(is_folder=False).select_related('parent'):
        files[f.get_full_path()] = f.content
    if file_id and file_id.isdigit():
        file_obj = project.files.filter(id=int(file_id), is_folder=False).first()
        if file_obj:
            entry = file_obj.get_full_path()
            if not code:
                code = file_obj.content
    if code or entry not in files:
        files[entry] = code  # muharrirdagi (hali saqlanmagan) kod ustun
    code = files.get(entry, '')

    if project.language == 'python' and not entry.endswith('.py'):
        # Tanlangan fayl (masalan, README.md) dastur emas — loyihaning kirish nuqtasini ishga tushiramiz
        py_files = sorted(name for name in files if name.endswith('.py'))
        entry = 'main.py' if 'main.py' in files else (py_files[0] if py_files else '')
        code = files.get(entry, '')
    if project.language == 'python' and not entry:
        output, success, elapsed_ms = (
            "[Xatolik] Loyihada ishga tushiriladigan .py fayli topilmadi.", False, 0
        )
    else:
        output, success, elapsed_ms = _execute_code_safely(
            project.language, code, files=files, entry=entry, stdin=stdin
        )

    return JsonResponse({
        'success': success,
        'output': output,
        'elapsed_ms': elapsed_ms,
    })


@login_required
@require_POST
def student_project_like_view(request, project_id):
    """Loyihaga layk bosish / qaytarib olish AJAX endpointi."""
    project = get_object_or_404(Project, id=project_id)
    like_obj = ProjectLike.objects.filter(user=request.user, project=project).first()

    if like_obj:
        like_obj.delete()
        is_liked = False
        project.likes_count = max(0, project.likes_count - 1)
    else:
        ProjectLike.objects.create(user=request.user, project=project)
        is_liked = True
        project.likes_count += 1

    project.save(update_fields=['likes_count'])
    return JsonResponse({
        'success': True,
        'is_liked': is_liked,
        'likes_count': project.likes_count,
    })
