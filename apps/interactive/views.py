import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from apps.core.code_runner import check_rate_limit, run_python
from apps.core.rendering import render_markdown
from apps.courses.models import Course, Lesson
from apps.learning.models import LessonProgress
from apps.learning.services import get_enrollment

from .grading import grade_task
from .models import (
    AssessmentAttempt,
    BLANK_TOKEN,
    BlockType,
    ModuleAssessment,
    Task,
    TaskAttempt,
    TaskKind,
    TaskSection,
)
from .services import (
    MAX_DRAFT_CHARS,
    assessment_status,
    can_manage_content,
    can_use_lesson,
    can_use_task,
    course_progress_summary,
    get_drafts,
    get_progress_map,
    record_assessment,
    record_lesson_attempt,
    reveal,
    reveal_rules,
    save_draft,
)

MAX_CODE_CHARS = 20_000
MAX_STDIN_CHARS = 5_000


def _json_body(request):
    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except (ValueError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def _bad(message, status=400):
    return JsonResponse({'ok': False, 'error': message}, status=status)


def snippet_parts(task):
    """Bo'sh joyli kodni [matn, None, matn, None, ...] bo'laklarga ajratadi (None — input joyi)."""
    pieces = (task.code_snippet or '').split(BLANK_TOKEN)
    parts = []
    for i, piece in enumerate(pieces):
        parts.append({'text': piece, 'blank': False})
        if i < len(pieces) - 1:
            parts.append({'text': '', 'blank': True, 'index': i})
    return parts


def build_task_view(task, progress):
    """Shablon uchun topshiriq ma'lumotlari (to'g'ri javoblar bu yerga KIRITILMAYDI)."""
    return {
        'obj': task,
        'prompt_html': render_markdown(task.prompt),
        'options': list(task.options.all()) if task.is_choice else [],
        'parts': snippet_parts(task) if task.kind == TaskKind.FILL_BLANK else [],
        'visible_tests': [t for t in task.tests.all() if not t.is_hidden] if task.uses_editor else [],
        'hidden_tests_count': sum(1 for t in task.tests.all() if t.is_hidden) if task.uses_editor else 0,
        'progress': progress,
        'rules': reveal_rules(task, progress),
        'is_solved': bool(progress and progress.is_solved),
    }


# ==============================================================================
# INTERAKTIV DARS SAHIFASI
# ==============================================================================

def render_interactive_lesson(request, base_context):
    """apps.learning.views.web_course_learn_view tomonidan interaktiv darslar uchun chaqiriladi."""
    lesson = base_context['current_lesson']
    course = base_context['course']
    user = request.user
    is_manager = can_manage_content(user)

    tasks_qs = (
        Task.objects.filter(lesson=lesson)
        .select_related('module__course', 'lesson')
        .prefetch_related('options', 'tests')
        .order_by('section', 'order', 'id')
    )
    if not is_manager:
        tasks_qs = tasks_qs.filter(is_published=True)
    tasks = list(tasks_qs)
    progress_map = get_progress_map(user, tasks)
    task_views = {t.id: build_task_view(t, progress_map.get(t.id)) for t in tasks}

    blocks = []
    embedded_task_ids = set()
    for block in lesson.blocks.select_related('task').order_by('order', 'id'):
        item = {'obj': block, 'html': render_markdown(block.body) if block.body else ''}
        if block.block_type == BlockType.TASK:
            tv = task_views.get(block.task_id)
            if not tv:
                continue
            item['task'] = tv
            embedded_task_ids.add(block.task_id)
        blocks.append(item)

    def by_section(*sections):
        return [task_views[t.id] for t in tasks if t.section in sections and t.id not in embedded_task_ids]

    practice = by_section(TaskSection.PRACTICE)
    difficulty_order = {'easy': 0, 'medium': 1, 'hard': 2}
    practice.sort(key=lambda tv: (difficulty_order.get(tv['obj'].difficulty, 9), tv['obj'].order))

    module = lesson.module
    assessment = ModuleAssessment.objects.filter(module=module).first()
    a_status = None
    if assessment and (assessment.is_published or is_manager):
        a_status = assessment_status(user, assessment, base_context.get('enrollment')) if user.is_authenticated else None
    else:
        assessment = None

    can_interact = can_use_lesson(user, lesson, base_context.get('enrollment')) if base_context.get('can_view') else False
    js_config = {
        'csrf': get_token(request),
        'lessonId': lesson.id,
        'canInteract': bool(can_interact),
        'isAuthenticated': user.is_authenticated,
        'loginUrl': f"{reverse('login')}?next={request.path}",
        'urls': {
            'run': reverse('interactive_run'),
            'check': reverse('interactive_task_check', args=[0]),
            'reveal': reverse('interactive_task_reveal', args=[0]),
            'attempts': reverse('interactive_task_attempts', args=[0]),
            'draft': reverse('interactive_draft_save'),
        },
        'drafts': get_drafts(user, lesson) if can_interact else {},
        'starters': {f"task-{t.id}": t.starter_code for t in tasks if t.uses_editor},
    }

    context = {
        **base_context,
        'module': module,
        'blocks': blocks,
        'quiz_tasks': by_section(TaskSection.QUIZ),
        'inline_tasks': by_section(TaskSection.INLINE),
        'assignment_tasks': by_section(TaskSection.ASSIGNMENT, TaskSection.PROJECT),
        'practice_tasks': practice,
        'review_tasks': by_section(TaskSection.REVIEW),
        'assessment': assessment,
        'assessment_status': a_status,
        'is_manager': is_manager,
        'is_draft_preview': not (lesson.is_published and module.is_published and course.is_published),
        'is_lesson_completed': lesson.id in base_context.get('completed_lesson_ids', set()),
        'js_config': js_config,
        'can_interact': can_interact,
    }
    return render(request, 'interactive/lesson.html', context)


# ==============================================================================
# AJAX: KODNI ISHGA TUSHIRISH
# ==============================================================================

@login_required
@require_POST
def run_code_view(request):
    data = _json_body(request)
    if data is None:
        return _bad("So'rov noto'g'ri.")
    code = data.get('code') or ''
    stdin = data.get('stdin') or ''
    if not isinstance(code, str) or not isinstance(stdin, str):
        return _bad("So'rov noto'g'ri.")
    if len(code) > MAX_CODE_CHARS or len(stdin) > MAX_STDIN_CHARS:
        return _bad("Kod hajmi juda katta.")

    # Ruxsat: dars yoki topshiriq konteksti majburiy
    lesson_id = data.get('lesson_id')
    task_id = data.get('task_id')
    allowed = False
    if task_id:
        task = Task.objects.select_related('lesson__module__course', 'module__course').filter(pk=task_id).first()
        if task:
            if task.lesson_id:
                allowed = can_use_task(request.user, task)
            else:
                assessment = ModuleAssessment.objects.filter(module=task.module, items__task=task).first()
                allowed = bool(assessment) and assessment_status(request.user, assessment)['can_attempt']
    elif lesson_id:
        lesson = Lesson.objects.select_related('module__course').filter(pk=lesson_id).first()
        allowed = bool(lesson) and can_use_lesson(request.user, lesson)
    if not allowed:
        return _bad("Bu kodni ishga tushirish uchun ruxsat yo'q. Kursga yozilganingizni tekshiring.", 403)

    if not check_rate_limit(request.user.id):
        return _bad("Juda ko'p ishga tushirish. Bir daqiqadan so'ng qayta urinib ko'ring.", 429)

    res = run_python(code, stdin=stdin)
    return JsonResponse({'ok': True, 'result': res.to_dict()})


# ==============================================================================
# AJAX: TOPSHIRIQNI TEKSHIRISH, YORDAM, URINISHLAR TARIXI
# ==============================================================================

def _get_task_for_user(request, task_id):
    task = get_object_or_404(
        Task.objects.select_related('lesson__module__course', 'module__course').prefetch_related('options', 'tests'),
        pk=task_id,
    )
    if not can_use_task(request.user, task):
        raise Http404
    return task


@login_required
@require_POST
def task_check_view(request, task_id):
    task = _get_task_for_user(request, task_id)
    data = _json_body(request)
    if data is None:
        return _bad("So'rov noto'g'ri.")
    code = data.get('code') or ''
    if not isinstance(code, str) or len(code) > MAX_CODE_CHARS:
        return _bad("Kod hajmi juda katta.")
    answer = {}
    if task.is_choice:
        options = data.get('options') or []
        if not isinstance(options, list):
            return _bad("So'rov noto'g'ri.")
        answer = {'options': options[:20]}
    elif task.kind == TaskKind.PREDICT_OUTPUT:
        answer = {'text': str(data.get('text') or '')[:5000]}
    elif task.kind == TaskKind.FILL_BLANK:
        blanks = data.get('blanks') or []
        if not isinstance(blanks, list):
            return _bad("So'rov noto'g'ri.")
        answer = {'blanks': [str(b)[:300] for b in blanks[:20]]}

    if (task.uses_editor or (task.kind == TaskKind.FILL_BLANK and task.tests.exists())) and not check_rate_limit(request.user.id):
        return _bad("Juda ko'p urinish. Bir daqiqadan so'ng qayta urinib ko'ring.", 429)

    grade = grade_task(task, answer, code)
    if grade.infrastructure_error:
        return JsonResponse({'ok': False, 'error': grade.message, 'infrastructure': True}, status=503)
    nothing_given = grade.score == 0 and not grade.is_correct and not grade.test_results and (
        grade.message in ("Javob variantini tanlang.", "Javobni yozing.", "Barcha bo'sh joylarni to'ldiring.",
                          "Kod bo'sh. Avval yechimingizni yozing.")
    )
    if nothing_given:
        return JsonResponse({'ok': False, 'error': grade.message}, status=400)

    attempt, progress, coins = record_lesson_attempt(request.user, task, grade, answer, code)
    rules = reveal_rules(task, progress)
    payload = {
        'ok': True,
        'is_correct': grade.is_correct,
        'score': grade.score,
        'max_score': grade.max_score,
        'message': grade.message,
        'tests': grade.test_results,
        'option_feedback': grade.option_feedback,
        'run': grade.run.to_dict() if grade.run else None,
        'attempt_number': attempt.attempt_number,
        'attempts': progress.attempts_count,
        'solved': progress.is_solved,
        'rules': rules,
        'coins_awarded': coins,
        'user_coins': request.user.coins,
    }
    # To'g'ri javobdan keyin tushuntirish darhol beriladi; noto'g'rida — faqat maslahat imkoniyati
    if grade.is_correct:
        payload['explanation_html'] = render_markdown(task.explanation) if task.explanation else ''
    return JsonResponse(payload)


@login_required
@require_POST
def task_reveal_view(request, task_id):
    task = _get_task_for_user(request, task_id)
    data = _json_body(request) or {}
    what = data.get('what')
    if what not in ('hint', 'partial', 'solution'):
        return _bad("So'rov noto'g'ri.")
    allowed, content, reason = reveal(request.user, task, what)
    if not allowed:
        return JsonResponse({'ok': False, 'error': reason}, status=403)
    if 'explanation' in content:
        content['explanation_html'] = render_markdown(content.pop('explanation') or '')
    return JsonResponse({'ok': True, 'what': what, **content})


@login_required
@require_GET
def task_attempts_view(request, task_id):
    task = _get_task_for_user(request, task_id)
    attempts = TaskAttempt.objects.filter(user=request.user, task=task, context='lesson').order_by('-created_at')[:20]
    return JsonResponse({
        'ok': True,
        'attempts': [
            {
                'number': a.attempt_number,
                'submitted_at': a.created_at.isoformat(),
                'is_correct': a.is_correct,
                'score': a.score,
                'max_score': a.max_score,
                'code': a.code,
                'answer': a.answer,
                'tests_passed': sum(1 for t in a.test_results if t.get('passed')),
                'tests_total': len(a.test_results),
            }
            for a in attempts
        ],
    })


@login_required
@require_POST
def draft_save_view(request):
    data = _json_body(request)
    if data is None:
        return _bad("So'rov noto'g'ri.")
    key = str(data.get('key') or '')
    code = data.get('code') or ''
    if not key or len(key) > 60 or not isinstance(code, str) or len(code) > MAX_DRAFT_CHARS:
        return _bad("So'rov noto'g'ri.")
    lesson = Lesson.objects.select_related('module__course').filter(pk=data.get('lesson_id')).first()
    if not lesson or not can_use_lesson(request.user, lesson):
        return _bad("Ruxsat yo'q.", 403)
    save_draft(request.user, lesson, key, code)
    return JsonResponse({'ok': True})


# ==============================================================================
# MODUL YAKUNIY NAZORATI
# ==============================================================================

def _assessment_or_404(request, assessment_id):
    assessment = get_object_or_404(
        ModuleAssessment.objects.select_related('module__course'), pk=assessment_id
    )
    if not can_manage_content(request.user):
        course = assessment.module.course
        if not (course.is_published and assessment.is_published and assessment.module.is_published):
            raise Http404
    return assessment


@login_required
def assessment_view(request, assessment_id):
    assessment = _assessment_or_404(request, assessment_id)
    course = assessment.module.course
    enrollment = get_enrollment(request.user, course)
    status = assessment_status(request.user, assessment, enrollment)
    items = list(assessment.ordered_items())

    if request.method == 'POST':
        if not status['can_attempt']:
            messages.error(request, status['reason'] or "Nazoratni hozir topshirib bo'lmaydi.")
            return redirect('interactive_assessment', assessment_id=assessment.id)
        if not check_rate_limit(request.user.id, scope='assessment'):
            messages.error(request, "Juda ko'p urinish. Birozdan so'ng qayta urinib ko'ring.")
            return redirect('interactive_assessment', assessment_id=assessment.id)

        graded = []
        for item in items:
            task = item.task
            answer, code = {}, ''
            key = f"t{task.id}"
            if task.is_choice:
                answer = {'options': request.POST.getlist(f"{key}_opt")[:20]}
            elif task.kind == TaskKind.PREDICT_OUTPUT:
                answer = {'text': request.POST.get(f"{key}_text", '')[:5000]}
            elif task.kind == TaskKind.FILL_BLANK:
                answer = {'blanks': [request.POST.get(f"{key}_b{i}", '')[:300] for i in range(task.blank_count)]}
            else:
                code = request.POST.get(f"{key}_code", '')[:MAX_CODE_CHARS]
            grade = grade_task(task, answer, code)
            if grade.infrastructure_error:
                messages.error(request, "Kod tekshirish xizmati vaqtincha ishlamayapti. Javoblaringiz saqlanmadi — birozdan so'ng qayta yuboring.")
                return redirect('interactive_assessment', assessment_id=assessment.id)
            graded.append((task, grade, answer, code))

        attempt, coins = record_assessment(request.user, assessment, graded)
        if attempt.passed:
            msg = f"Tabriklaymiz! Siz nazoratdan {attempt.percent:.0f}% natija bilan o'tdingiz."
            if coins:
                msg += f" +{coins} tanga."
            messages.success(request, msg)
        else:
            messages.warning(request, f"Natija: {attempt.percent:.0f}%. O'tish uchun {attempt.pass_percent}% kerak. Xatolarni ko'rib chiqib, qayta topshiring.")
        return redirect('interactive_assessment_result', attempt_id=attempt.id)

    task_views = [build_task_view(item.task, None) for item in items]
    context = {
        'assessment': assessment,
        'module': assessment.module,
        'course': course,
        'status': status,
        'task_views': task_views,
        'description_html': render_markdown(assessment.description),
        'history': AssessmentAttempt.objects.filter(user=request.user, assessment=assessment).order_by('-created_at')[:10],
        'js_config': {
            'canInteract': status['can_attempt'],
            'urls': {'run': reverse('interactive_run')},
            'starters': {f"task-{tv['obj'].id}": tv['obj'].starter_code for tv in task_views if tv['obj'].uses_editor},
        },
        'active_menu': 'courses',
    }
    return render(request, 'interactive/assessment.html', context)


@login_required
def assessment_result_view(request, attempt_id):
    attempt = get_object_or_404(
        AssessmentAttempt.objects.select_related('assessment__module__course'), pk=attempt_id, user=request.user
    )
    answers = {a.task_id: a for a in attempt.answers.select_related('task').prefetch_related('task__options')}
    rows = []
    for item in attempt.assessment.ordered_items():
        task = item.task
        ans = answers.get(task.id)
        selected = set()
        if ans and task.is_choice:
            selected = {int(x) for x in (ans.answer or {}).get('options', []) if str(x).isdigit()}
        rows.append({
            'task': task,
            'answer': ans,
            'prompt_html': render_markdown(task.prompt),
            'explanation_html': render_markdown(task.explanation) if task.explanation else '',
            'options': [{'obj': o, 'selected': o.id in selected} for o in task.options.all()] if task.is_choice else [],
        })
    return render(request, 'interactive/assessment_result.html', {
        'attempt': attempt,
        'assessment': attempt.assessment,
        'course': attempt.assessment.module.course,
        'rows': rows,
        'show_solutions': attempt.passed,
    })


# ==============================================================================
# O'QUVCHI PROGRESSI
# ==============================================================================

@login_required
def course_progress_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not course.is_published and not can_manage_content(request.user):
        raise Http404
    summary = course_progress_summary(request.user, course)
    if not summary['enrollment'] and not can_manage_content(request.user):
        messages.info(request, "Progressni ko'rish uchun avval kursga yoziling.")
        return redirect('course_detail', slug=course.slug)
    recent_attempts = (
        TaskAttempt.objects.filter(user=request.user, task__module__course=course)
        .select_related('task__lesson', 'task__module')
        .order_by('-created_at')[:15]
    )
    assessment_attempts = (
        AssessmentAttempt.objects.filter(user=request.user, assessment__module__course=course)
        .select_related('assessment__module')
        .order_by('-created_at')[:10]
    )
    return render(request, 'interactive/progress.html', {
        'course': course,
        'summary': summary,
        'recent_attempts': recent_attempts,
        'assessment_attempts': assessment_attempts,
        'active_menu': 'dashboard',
    })


@login_required
def my_learning_view(request):
    """Talabaning barcha interaktiv kurslari ro'yxati (progress panelga kirish nuqtasi)."""
    from apps.learning.models import Enrollment
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    rows = []
    for e in enrollments:
        if not e.course.is_published:
            continue
        rows.append({
            'enrollment': e,
            'course': e.course,
            'done': LessonProgress.objects.filter(enrollment=e, lesson__is_published=True).count(),
            'total': e.course.lessons_count,
        })
    return render(request, 'interactive/my_learning.html', {'rows': rows, 'active_menu': 'dashboard'})
