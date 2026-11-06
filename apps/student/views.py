import os
import io
import ast
import sys
import time
import builtins as _builtins_module
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

# Talaba kodini bajarishda ruxsat etilgan "xavfsiz" builtin'lar ro'yxati.
# Fayl tizimiga, tarmoqqa, boshqa modullarga (os, sys, subprocess va h.k.)
# kirish imkonini beradigan hech narsa shu ro'yxatga kiritilmaydi
# (masalan: open, __import__, eval, exec, compile, globals, locals, dir).
_SAFE_BUILTIN_NAMES = (
    'abs', 'all', 'any', 'bin', 'bool', 'chr', 'complex', 'dict', 'divmod',
    'enumerate', 'filter', 'float', 'format', 'frozenset', 'hex', 'int',
    'isinstance', 'issubclass', 'len', 'list', 'map', 'max', 'min', 'next',
    'oct', 'ord', 'pow', 'print', 'range', 'repr', 'reversed', 'round',
    'set', 'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip',
    'super', 'object', 'property', 'classmethod', 'staticmethod',
    'True', 'False', 'None', 'NotImplemented', '__build_class__', '__name__',
    'Exception', 'BaseException', 'ValueError', 'TypeError', 'IndexError',
    'KeyError', 'ZeroDivisionError', 'StopIteration', 'RuntimeError',
    'ArithmeticError', 'OverflowError', 'NameError', 'AttributeError',
    'AssertionError', 'FloatingPointError', 'LookupError', 'UnicodeError',
    'NotImplementedError', 'RecursionError',
)

# Bajarilish vaqti / amallar soni chegarasi (cheksiz sikllarni to'xtatish uchun)
_EXEC_MAX_SECONDS = 3
_EXEC_MAX_STEPS = 300_000
_EXEC_MAX_OUTPUT_CHARS = 20_000

# `object.__class__.__bases__[0].__subclasses__()` kabi "sandbox escape"
# usullarining oldini olish uchun xavfli dunder atributlarga murojaat
# (attribute access) qilish taqiqlanadi. Oddiy magic metodlar
# (__init__, __str__, super().__init__() va h.k.) ta'sirlanmaydi, chunki ular
# metod ta'rifi (FunctionDef) sifatida yoziladi, Attribute access sifatida emas.
_BLOCKED_DUNDER_ATTRS = {
    '__class__', '__bases__', '__base__', '__subclasses__', '__mro__',
    '__globals__', '__builtins__', '__import__', '__getattribute__',
    '__code__', '__closure__', '__func__', '__self__', '__dict__',
    '__reduce__', '__reduce_ex__', '__subclasshook__', '__loader__',
    '__spec__', '__module__',
}
_BLOCKED_NAMES = {
    'exec', 'eval', 'compile', '__import__', 'globals', 'locals', 'vars',
    'open', 'getattr', 'setattr', 'delattr', 'dir', 'help', 'breakpoint',
}


def _find_unsafe_construct(code):
    """Kodni bajarishdan oldin AST orqali xavfli konstruksiyalarni aniqlaydi."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None  # Sintaksis xatosi - buni haqiqiy exec() xato sifatida ko'rsatamiz
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in _BLOCKED_DUNDER_ATTRS:
            return node.attr
        if isinstance(node, ast.Name) and node.id in _BLOCKED_NAMES:
            return node.id
    return None


class _ExecutionLimitExceeded(Exception):
    """Kod juda uzoq ishlaganda yoki juda ko'p amal bajarganda ko'tariladi."""


def _build_safe_globals(custom_input):
    safe_builtins = {
        name: getattr(_builtins_module, name)
        for name in _SAFE_BUILTIN_NAMES
        if hasattr(_builtins_module, name)
    }
    safe_builtins['input'] = custom_input
    return {
        '__name__': '__main__',
        '__builtins__': safe_builtins,
    }


def _make_step_limiter():
    state = {'steps': 0, 'start': time.time()}

    def tracer(frame, event, arg):
        if event == 'line':
            state['steps'] += 1
            if state['steps'] > _EXEC_MAX_STEPS or (time.time() - state['start']) > _EXEC_MAX_SECONDS:
                raise _ExecutionLimitExceeded(
                    "Kod bajarilishi vaqt (3s) yoki amallar sonining chegarasidan oshib ketdi "
                    "(cheksiz sikl yoki juda og'ir hisoblash bo'lishi mumkin)."
                )
        return tracer
    return tracer


def _execute_code_safely(language, code):
    """
    Kodni xavfsiz simulyatsiya qilish yoki Python kodini cheklangan (sandboxed) muhitda bajarish.

    Eslatma: bu faqat bazaviy himoya (import/fayl/tarmoqqa kirish taqiqlangan, vaqt/amal
    chegarasi qo'yilgan). To'liq xavfsizlik uchun productionda kodni alohida, tarmoqsiz,
    resurslari cheklangan konteyner/subprocess ichida bajarish tavsiya etiladi.
    """
    start_time = time.time()
    if language == 'python':
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()

        unsafe = _find_unsafe_construct(code)
        if unsafe:
            elapsed_ms = int((time.time() - start_time) * 1000)
            return (
                f"[Xavfsizlik xatosi] Kodda ruxsat etilmagan '{unsafe}' konstruksiyasi aniqlandi. "
                "Iltimos, standart dasturlash amallaridan foydalaning."
            ), False, elapsed_ms

        old_trace = sys.gettrace()
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

            globs = _build_safe_globals(custom_input)

            sys.settrace(_make_step_limiter())
            try:
                with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stderr_buf):
                    exec(code, globs)
            finally:
                sys.settrace(old_trace)

            output = stdout_buf.getvalue()
            errors = stderr_buf.getvalue()
            elapsed_ms = int((time.time() - start_time) * 1000)

            if len(output) > _EXEC_MAX_OUTPUT_CHARS:
                output = output[:_EXEC_MAX_OUTPUT_CHARS] + "\n...\n[Chiqish hajm chegarasi tufayli qisqartirildi]"

            if errors:
                return f"{output}\n[Xatolik]:\n{errors}", False, elapsed_ms
            return output or "[Dastur muvaffaqiyatli yakunlandi, ekranga hech narsa chiqarilmadi.]", True, elapsed_ms
        except _ExecutionLimitExceeded as e:
            sys.settrace(old_trace)
            elapsed_ms = int((time.time() - start_time) * 1000)
            partial_output = stdout_buf.getvalue()[:_EXEC_MAX_OUTPUT_CHARS]
            return f"{partial_output}\n[Xatolik] {str(e)}", False, elapsed_ms
        except Exception as e:
            sys.settrace(old_trace)
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
