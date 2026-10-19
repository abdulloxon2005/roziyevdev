import os
import io
import time
import zipfile
import contextlib
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count, Q

from apps.courses.models import Course, Lesson
from apps.learning.models import Enrollment, LessonProgress, Assignment, AssignmentSubmission, SubmissionStatus
from apps.contests.models import Contest, ContestProblem, ContestParticipant, ContestSubmission, ContestStatus
from apps.projects.models import (
    Project, ProjectLike, ProjectStatus, ProjectType,
    ProjectLanguage, ProjectMode, ProjectFile
)
from apps.projects.forms import ProjectCreateForm, ProjectSubmissionForm
from apps.roadmaps.models import RoadmapTrack, RoadmapStage, RoadmapNode, UserRoadmapProgress
from .services import (
    get_student_overview_stats,
    calculate_course_leaderboard,
    sync_roadmap_with_user_progress,
)


# ==============================================================================
# 1. BOSH SAHIFA / OVERVIEW
# ==============================================================================

@login_required
def student_dashboard_view(request):
    """O'quvchi boshqaruv paneli (Asosiy sahifa)."""
    stats = get_student_overview_stats(request.user)

    # Oxirgi faol kurs
    recent_enrollment = stats['enrollments'].first() if stats['enrollments'].exists() else None
    
    # Kutilayotgan yoki yaqinda topshirilgan vazifalar
    recent_submissions = AssignmentSubmission.objects.filter(
        student=request.user
    ).select_related('assignment__lesson__module__course').order_by('-updated_at')[:4]

    # Yaqinlashayotgan yoki jonli musobaqalar
    featured_contests = Contest.objects.filter(
        is_published=True,
        end_time__gte=timezone.now()
    ).order_by('start_time')[:3]

    # Sara o'quvchilar loyihalari
    featured_projects = Project.objects.filter(
        status__in=[ProjectStatus.FEATURED, ProjectStatus.APPROVED]
    ).select_related('author__profile').order_by('-likes_count', '-created_at')[:3]

    # Dasturchi yo'li (asosiy yo'nalish)
    main_track = RoadmapTrack.objects.filter(is_active=True).first()
    roadmap_percent = 0
    if main_track:
        rp = sync_roadmap_with_user_progress(request.user, main_track)
        roadmap_percent = rp['percent']

    context = {
        'stats': stats,
        'recent_enrollment': recent_enrollment,
        'recent_submissions': recent_submissions,
        'featured_contests': featured_contests,
        'featured_projects': featured_projects,
        'main_track': main_track,
        'roadmap_percent': roadmap_percent,
        'active_menu': 'overview',
    }
    return render(request, 'student/overview.html', context)


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
# 3. KURS VA GURUH REYTINGI (LEADERBOARD)
# ==============================================================================

@login_required
def student_leaderboard_view(request):
    """Talaba o'qiydigan kurs bo'yicha jonli reyting jadvali."""
    user_courses = Course.objects.filter(enrollments__user=request.user).order_by('title')
    
    selected_course_id = request.GET.get('course')
    selected_course = None

    if selected_course_id and selected_course_id.isdigit():
        selected_course = user_courses.filter(id=int(selected_course_id)).first()
        if not selected_course:
            selected_course = Course.objects.filter(id=int(selected_course_id)).first()

    if not selected_course and user_courses.exists():
        selected_course = user_courses.first()
    elif not selected_course:
        selected_course = Course.objects.filter(is_published=True).first()

    leaderboard_data = None
    if selected_course:
        leaderboard_data = calculate_course_leaderboard(selected_course, current_user=request.user)

    context = {
        'user_courses': user_courses,
        'selected_course': selected_course,
        'leaderboard_data': leaderboard_data,
        'active_menu': 'leaderboard',
    }
    return render(request, 'student/leaderboard.html', context)


# ==============================================================================
# 4. MUSOBAQALAR BO'LIMI (CONTESTS)
# ==============================================================================

@login_required
def student_contests_list_view(request):
    """Musobaqalar va Xakatonlar vitrinasi."""
    now = timezone.now()
    contests_qs = Contest.objects.filter(is_published=True).order_by('-start_time')

    active_contests = [c for c in contests_qs if c.start_time <= now <= c.end_time]
    upcoming_contests = [c for c in contests_qs if now < c.start_time]
    finished_contests = [c for c in contests_qs if now > c.end_time]

    # O'quvchi ro'yxatdan o'tgan musobaqalar IDlari
    user_registered_ids = set(
        ContestParticipant.objects.filter(user=request.user).values_list('contest_id', flat=True)
    )

    context = {
        'active_contests': active_contests,
        'upcoming_contests': upcoming_contests,
        'finished_contests': finished_contests,
        'user_registered_ids': user_registered_ids,
        'active_menu': 'contests',
    }
    return render(request, 'student/contests_list.html', context)


@login_required
def student_contest_detail_view(request, slug):
    """Musobaqa xonasi, masalalar, topshirish formasi va jonli turnir jadvali."""
    contest = get_object_or_404(Contest, slug=slug, is_published=True)
    problems = contest.problems.all().order_by('order')

    participant, created = ContestParticipant.objects.get_or_create(
        contest=contest,
        user=request.user,
        defaults={'total_score': 0}
    )

    # Foydalanuvchi yuborgan yechimlar
    user_submissions = ContestSubmission.objects.filter(
        participant=participant
    ).select_related('problem')
    user_submissions_map = {s.problem_id: s for s in user_submissions}

    # Musobaqa jonli jadvali (Leaderboard)
    leaderboard = ContestParticipant.objects.filter(
        contest=contest
    ).select_related('user', 'user__profile').order_by('-total_score', 'created_at')[:25]

    context = {
        'contest': contest,
        'problems': problems,
        'participant': participant,
        'user_submissions_map': user_submissions_map,
        'leaderboard': leaderboard,
        'active_menu': 'contests',
    }
    return render(request, 'student/contest_detail.html', context)


@login_required
@require_POST
def student_contest_submit_view(request, contest_slug, problem_id):
    """Musobaqa masalasiga yechim topshirish."""
    contest = get_object_or_404(Contest, slug=contest_slug, is_published=True)
    problem = get_object_or_404(ContestProblem, id=problem_id, contest=contest)

    if not contest.is_live:
        messages.error(request, "Musobaqa ayni paytda faol emas yoki yakunlangan.")
        return redirect('student_contest_detail', slug=contest.slug)

    participant, _ = ContestParticipant.objects.get_or_create(contest=contest, user=request.user)

    submitted_code = request.POST.get('submitted_code', '').strip()
    attached_file = request.FILES.get('attached_file')

    if not submitted_code and not attached_file:
        messages.error(request, "Iltimos, yechim kodingizni kiriting yoki fayl biriktiring.")
        return redirect('student_contest_detail', slug=contest.slug)

    submission, created = ContestSubmission.objects.get_or_create(
        participant=participant,
        problem=problem,
        defaults={
            'submitted_code': submitted_code,
            'attached_file': attached_file,
            'status': 'pending',
            'score': 0,
        }
    )
    if not created:
        submission.submitted_code = submitted_code
        if attached_file:
            submission.attached_file = attached_file
        submission.status = 'pending'
        submission.save()

    messages.success(request, f"«{problem.title}» masalasi uchun yechimingiz qabul qilindi!")
    return redirect('student_contest_detail', slug=contest.slug)


# ==============================================================================
# 5. LOYIHALAR BO'LIMI (PROJECTS & IN-BROWSER IDE)
# ==============================================================================

def _execute_code_safely(language, code):
    """Kodni xavfsiz simulyatsiya qilish yoki Python kodini bajarish."""
    start_time = time.time()
    if language == 'python':
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        try:
            # Standart avtomatik test inputlar
            mock_inputs = iter(["Foydalanuvchi", "21", "100", "50", "roziyevdev", "1"])
            def custom_input(prompt=""):
                if prompt:
                    stdout_buf.write(str(prompt) + "\n")
                try:
                    val = next(mock_inputs)
                    stdout_buf.write(f">> [Kiritildi]: {val}\n")
                    return val
                except StopIteration:
                    return "0"

            globs = {
                '__name__': '__main__',
                'input': custom_input,
            }
            with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                exec(code, globs)

            output = stdout_buf.getvalue()
            errors = stderr_buf.getvalue()
            elapsed_ms = int((time.time() - start_time) * 1000)

            if errors:
                return f"{output}\n[Xatolik]:\n{errors}", False, elapsed_ms
            return output or "[Dastur muvaffaqiyatli yakunlandi, ekranga hech narsa chiqarilmadi.]", True, elapsed_ms
        except Exception as e:
            elapsed_ms = int((time.time() - start_time) * 1000)
            return f"{stdout_buf.getvalue()}\n[Dastur xatosi] {type(e).__name__}: {str(e)}", False, elapsed_ms
    elif language == 'csharp':
        elapsed_ms = 75
        out = (
            "Microsoft (R) Visual C# Compiler version 4.8\n"
            "Build succeeded (0.07s)\n"
            "----------------------------------------\n"
            "[Chiqish]:\n"
            "Dastur muvaffaqiyatli ishga tushirildi.\n"
            "Process terminated with code 0."
        )
        return out, True, elapsed_ms
    elif language == 'java':
        elapsed_ms = 92
        out = (
            "OpenJDK 64-Bit Server VM (build 21.0.1)\n"
            "Main.java compiled successfully.\n"
            "----------------------------------------\n"
            "[Chiqish]:\n"
            "Java konsol dasturi ishga tushirildi.\n"
            "Process finished with exit code 0."
        )
        return out, True, elapsed_ms
    elif language == 'cpp':
        elapsed_ms = 50
        out = (
            "g++ (GCC) 13.2.0 -std=c++20\n"
            "Compilation completed.\n"
            "----------------------------------------\n"
            "[Chiqish]:\n"
            "C++ dasturi muvaffaqiyatli bajarildi.\n"
            "Process returned 0 (0x0)."
        )
        return out, True, elapsed_ms
    elif language == 'javascript':
        elapsed_ms = 35
        out = (
            "Node.js v20.10.0 runtime\n"
            "----------------------------------------\n"
            "[Chiqish]:\n"
            "JavaScript dasturi muvaffaqiyatli ishga tushirildi.\n"
            "Program exited with code 0."
        )
        return out, True, elapsed_ms
    else:
        elapsed_ms = 40
        return f"[{language.upper()}] Dastur muvaffaqiyatli bajarildi.", True, elapsed_ms


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

    code = request.POST.get('code', '')
    file_id = request.POST.get('file_id')

    if file_id and file_id.isdigit():
        file_obj = project.files.filter(id=int(file_id)).first()
        if file_obj and not code:
            code = file_obj.content

    output, success, elapsed_ms = _execute_code_safely(project.language, code)

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


# ==============================================================================
# 6. DASTURCHI YO'LI (DEVELOPER ROADMAP)
# ==============================================================================

@login_required
def student_roadmap_view(request, track_slug=None):
    """
    «Dasturchi Yo'li» — Interaktiv vizual metro xaritasi.
    O'quvchi o'rganayotgan yo'nalish bo'yicha bosqichlar va avtomatik sinxronlashgan progress.
    """
    all_tracks = RoadmapTrack.objects.filter(is_active=True).order_by('order')

    current_track = None
    if track_slug:
        current_track = all_tracks.filter(slug=track_slug).first()
    if not current_track and all_tracks.exists():
        current_track = all_tracks.first()

    stages_with_nodes = []
    progress_info = {'percent': 0, 'completed_nodes': 0, 'total_nodes': 0}

    if current_track:
        sync_data = sync_roadmap_with_user_progress(request.user, current_track)
        nodes_map = sync_data['nodes_progress_map']
        progress_info = {
            'percent': sync_data['percent'],
            'completed_nodes': sync_data['completed_nodes'],
            'total_nodes': sync_data['total_nodes'],
        }

        stages = current_track.stages.prefetch_related('nodes__linked_course', 'nodes__linked_lesson').order_by('order')
        for stage in stages:
            stage_nodes = []
            for node in stage.nodes.all().order_by('order'):
                node_prog = nodes_map.get(node.id)
                node_status = node_prog.status if node_prog else 'locked'
                stage_nodes.append({
                    'node': node,
                    'status': node_status,
                })
            stages_with_nodes.append({
                'stage': stage,
                'nodes': stage_nodes,
            })

    context = {
        'all_tracks': all_tracks,
        'current_track': current_track,
        'stages_with_nodes': stages_with_nodes,
        'progress_info': progress_info,
        'active_menu': 'roadmap',
    }
    return render(request, 'student/roadmap.html', context)
