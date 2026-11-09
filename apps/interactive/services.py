"""Interaktiv ta'lim biznes-mantiqi: ruxsatlar, urinishlarni saqlash, progress, nazorat."""
from django.db import transaction
from django.utils import timezone

from apps.courses.models import Lesson
from apps.learning.models import CoinTransaction, Enrollment, LessonProgress
from apps.learning.services import can_access_lesson, get_enrollment

from .models import (
    AssessmentAttempt,
    AttemptContext,
    CodeDraft,
    ModuleAssessment,
    Task,
    TaskAttempt,
    TaskProgress,
    TaskProgressStatus,
    TaskSection,
)

MAX_STORED_OUTPUT = 5000
MAX_DRAFT_CHARS = 50_000

# Mukofot tangalari (mavjud gamifikatsiya tizimi bilan integratsiya)
COINS_FOR_ASSIGNMENT = 20
COINS_FOR_PROJECT = 50
COINS_FOR_ASSESSMENT = 100


# ==============================================================================
# RUXSATLAR
# ==============================================================================

def can_manage_content(user):
    """Kurs kontentini tahrirlash va qoralamalarni ko'rish huquqi (admin / o'qituvchi / staff)."""
    return bool(
        user.is_authenticated and (
            user.is_superuser or user.is_staff or getattr(user, 'role', '') in ('admin', 'instructor')
        )
    )


def is_lesson_published(lesson):
    return lesson.is_published and lesson.module.is_published


def published_course_lessons(course, include_drafts=False):
    qs = Lesson.objects.filter(module__course=course).select_related('module')
    if not include_drafts:
        qs = qs.filter(is_published=True, module__is_published=True)
    return list(qs.order_by('module__order', 'module__id', 'order', 'id'))


def can_use_lesson(user, lesson, enrollment=None):
    """O'quvchi dars interaktiv elementlaridan foydalana oladimi (nashr + ruxsat)."""
    if not user.is_authenticated:
        return False
    if can_manage_content(user):
        return True
    if not is_lesson_published(lesson):
        return False
    if enrollment is None:
        enrollment = get_enrollment(user, lesson.module.course)
    return can_access_lesson(user, lesson, enrollment)


def can_use_task(user, task):
    """Topshiriqni dars kontekstida tekshirish/ko'rish mumkinmi."""
    if not user.is_authenticated:
        return False
    if can_manage_content(user):
        return True
    if not task.is_published or not task.module.is_published:
        return False
    if task.lesson_id:
        return can_use_lesson(user, task.lesson)
    return False  # nazorat savollari faqat nazorat sahifasi orqali


# ==============================================================================
# URINISHLAR VA HOLAT
# ==============================================================================

def get_progress_map(user, tasks):
    if not user.is_authenticated:
        return {}
    ids = [t.id for t in tasks]
    return {p.task_id: p for p in TaskProgress.objects.filter(user=user, task_id__in=ids)}


def _award_coins(user, amount, description):
    if amount <= 0:
        return
    user.add_coins(amount)
    CoinTransaction.objects.create(student=user, amount=amount, description=description)


@transaction.atomic
def record_lesson_attempt(user, task, grade, answer, code=''):
    """Dars ichidagi topshiriq urinishini saqlaydi va TaskProgress'ni yangilaydi."""
    progress, _ = TaskProgress.objects.select_for_update().get_or_create(user=user, task=task)
    progress.attempts_count += 1
    progress.best_score = max(progress.best_score, grade.score)
    newly_solved = False
    if grade.is_correct and progress.status != TaskProgressStatus.SOLVED:
        progress.status = TaskProgressStatus.SOLVED
        progress.solved_at = timezone.now()
        newly_solved = True
    progress.save()

    attempt = TaskAttempt.objects.create(
        user=user,
        task=task,
        context=AttemptContext.LESSON,
        attempt_number=progress.attempts_count,
        answer=answer or {},
        code=code or '',
        is_correct=grade.is_correct,
        score=grade.score,
        max_score=grade.max_score,
        test_results=grade.test_results,
        output=(grade.run.stdout if grade.run else '')[:MAX_STORED_OUTPUT],
    )

    coins = 0
    if newly_solved and not progress.solution_viewed:
        if task.section == TaskSection.ASSIGNMENT:
            coins = COINS_FOR_ASSIGNMENT
        elif task.section == TaskSection.PROJECT:
            coins = COINS_FOR_PROJECT
        if coins:
            _award_coins(user, coins, f"«{task.title}» vazifasi mustaqil yechilgani uchun")
    return attempt, progress, coins


def reveal_rules(task, progress):
    """Qaysi yordam materiallari ochiq ekanini qaytaradi."""
    attempts = progress.attempts_count if progress else 0
    solved = bool(progress and progress.is_solved)
    return {
        'hint': bool(task.hint),
        'partial': bool(task.partial_solution) and (attempts >= 1 or solved),
        'solution': (attempts >= task.solution_unlock_attempts) or solved,
        'attempts': attempts,
        'attempts_needed': max(0, task.solution_unlock_attempts - attempts),
    }


@transaction.atomic
def reveal(user, task, what):
    """
    Maslahat / qisman yechim / to'liq yechim (javob) ni ochish.
    Qaytaradi: (ruxsat_berildimi, ma'lumot_dict, sabab)
    """
    progress, _ = TaskProgress.objects.select_for_update().get_or_create(user=user, task=task)
    rules = reveal_rules(task, progress)
    if what == 'hint':
        if not rules['hint']:
            return False, {}, "Bu topshiriq uchun maslahat yo'q."
        progress.hint_viewed = True
        progress.save(update_fields=['hint_viewed', 'updated_at'])
        return True, {'hint': task.hint}, ''
    if what == 'partial':
        if not task.partial_solution:
            return False, {}, "Bu topshiriq uchun qisman yechim yo'q."
        if not rules['partial']:
            return False, {}, "Qisman yechimni ko'rish uchun avval kamida bir marta o'zingiz urinib ko'ring."
        progress.partial_viewed = True
        progress.save(update_fields=['partial_viewed', 'updated_at'])
        return True, {'partial': task.partial_solution}, ''
    if what == 'solution':
        if not rules['solution']:
            return False, {}, (
                f"To'liq yechim {task.solution_unlock_attempts} ta mustaqil urinishdan keyin ochiladi. "
                f"Yana {rules['attempts_needed']} marta urinib ko'ring — maslahatdan foydalaning."
            )
        progress.solution_viewed = True
        progress.save(update_fields=['solution_viewed', 'updated_at'])
        return True, solution_payload(task), ''
    return False, {}, "Noma'lum so'rov."


def solution_payload(task):
    data = {'explanation': task.explanation}
    if task.is_choice:
        data['correct_options'] = list(task.options.filter(is_correct=True).values_list('id', flat=True))
    elif task.kind == 'predict_output':
        data['correct_answer'] = task.correct_answer
    elif task.kind == 'fill_blank':
        data['correct_blanks'] = [alts[0] if alts else '' for alts in task.accepted_blank_answers]
    if task.full_solution:
        data['solution'] = task.full_solution
    return data


# ==============================================================================
# QORALAMALAR (AUTOSAVE)
# ==============================================================================

def save_draft(user, lesson, key, code):
    code = (code or '')[:MAX_DRAFT_CHARS]
    CodeDraft.objects.update_or_create(user=user, lesson=lesson, key=key[:60], defaults={'code': code})


def get_drafts(user, lesson):
    if not user.is_authenticated:
        return {}
    return dict(CodeDraft.objects.filter(user=user, lesson=lesson).values_list('key', 'code'))


# ==============================================================================
# MODUL NAZORATI
# ==============================================================================

def module_lesson_stats(module, enrollment):
    lessons = list(module.lessons.filter(is_published=True).values_list('id', flat=True))
    done = 0
    if enrollment:
        done = LessonProgress.objects.filter(enrollment=enrollment, lesson_id__in=lessons).count()
    return done, len(lessons)


def assessment_status(user, assessment, enrollment=None):
    """Nazorat holati: ochiqmi, nega yopiq, urinishlar, eng yaxshi natija."""
    module = assessment.module
    if enrollment is None and user.is_authenticated:
        enrollment = get_enrollment(user, module.course)
    done, total = module_lesson_stats(module, enrollment)
    attempts = list(AssessmentAttempt.objects.filter(user=user, assessment=assessment)) if user.is_authenticated else []
    best = max(attempts, key=lambda a: a.percent, default=None)
    status = {
        'lessons_done': done,
        'lessons_total': total,
        'attempts_used': len(attempts),
        'best': best,
        'passed': any(a.passed for a in attempts),
        'unlocked': True,
        'reason': '',
        'can_attempt': True,
    }
    manager = can_manage_content(user)
    if not manager:
        if not user.is_authenticated or enrollment is None:
            status.update(unlocked=False, can_attempt=False, reason="Nazoratni topshirish uchun kursga yozilishingiz kerak.")
        elif not assessment.is_published or not module.is_published:
            status.update(unlocked=False, can_attempt=False, reason="Nazorat hali nashr qilinmagan.")
        elif assessment.require_all_lessons and done < total:
            status.update(unlocked=False, can_attempt=False,
                          reason=f"Nazorat barcha darslar tugagach ochiladi ({done}/{total} dars tugallangan).")
    if status['unlocked'] and assessment.max_attempts and len(attempts) >= assessment.max_attempts and not manager:
        status.update(can_attempt=False, reason="Urinishlar soni tugagan.")
    return status


@transaction.atomic
def record_assessment(user, assessment, graded_items):
    """
    graded_items: [(task, grade, answer, code), ...]
    """
    previous = AssessmentAttempt.objects.select_for_update().filter(user=user, assessment=assessment)
    already_passed = previous.filter(passed=True).exists()
    number = previous.count() + 1
    score = sum(g.score for _, g, _, _ in graded_items)
    max_score = sum(g.max_score for _, g, _, _ in graded_items)
    percent = round(score * 100 / max_score, 1) if max_score else 0
    attempt = AssessmentAttempt.objects.create(
        user=user,
        assessment=assessment,
        attempt_number=number,
        score=round(score, 2),
        max_score=max_score,
        percent=percent,
        pass_percent=assessment.pass_percent,
        passed=percent >= assessment.pass_percent,
    )
    for task, grade, answer, code in graded_items:
        TaskAttempt.objects.create(
            user=user,
            task=task,
            context=AttemptContext.ASSESSMENT,
            assessment_attempt=attempt,
            attempt_number=number,
            answer=answer or {},
            code=code or '',
            is_correct=grade.is_correct,
            score=grade.score,
            max_score=grade.max_score,
            test_results=grade.test_results,
            output=(grade.run.stdout if grade.run else '')[:MAX_STORED_OUTPUT],
        )
    coins = 0
    if attempt.passed and not already_passed:
        coins = COINS_FOR_ASSESSMENT
        _award_coins(user, coins, f"«{assessment.title}» nazoratidan muvaffaqiyatli o'tgani uchun")
    return attempt, coins


# ==============================================================================
# O'QUVCHI PANELI UCHUN UMUMIY PROGRESS
# ==============================================================================

def course_progress_summary(user, course):
    enrollment = get_enrollment(user, course)
    completed_ids = set()
    if enrollment:
        completed_ids = set(LessonProgress.objects.filter(enrollment=enrollment).values_list('lesson_id', flat=True))

    modules = []
    all_tasks = list(
        Task.objects.filter(module__course=course, is_published=True, lesson__isnull=False)
        .select_related('lesson')
    )
    progress_map = get_progress_map(user, all_tasks)
    tasks_by_lesson = {}
    for t in all_tasks:
        tasks_by_lesson.setdefault(t.lesson_id, []).append(t)

    total_lessons = 0
    total_done = 0
    for module in course.modules.filter(is_published=True).order_by('order', 'id'):
        lessons = []
        for lesson in module.lessons.filter(is_published=True).order_by('order', 'id'):
            ltasks = tasks_by_lesson.get(lesson.id, [])
            quiz = [t for t in ltasks if t.section in (TaskSection.QUIZ, TaskSection.REVIEW)]
            assignments = [t for t in ltasks if t.section in (TaskSection.ASSIGNMENT, TaskSection.PROJECT)]
            quiz_solved = sum(1 for t in quiz if progress_map.get(t.id) and progress_map[t.id].is_solved)
            assign_rows = []
            for t in assignments:
                p = progress_map.get(t.id)
                assign_rows.append({
                    'task': t,
                    'progress': p,
                    'status': 'solved' if p and p.is_solved else ('attempted' if p else 'new'),
                })
            lessons.append({
                'lesson': lesson,
                'completed': lesson.id in completed_ids,
                'quiz_total': len(quiz),
                'quiz_solved': quiz_solved,
                'assignments': assign_rows,
            })
            total_lessons += 1
            total_done += 1 if lesson.id in completed_ids else 0
        assessment = ModuleAssessment.objects.filter(module=module).first()
        a_status = assessment_status(user, assessment, enrollment) if assessment else None
        modules.append({'module': module, 'lessons': lessons, 'assessment': assessment, 'assessment_status': a_status})

    return {
        'enrollment': enrollment,
        'modules': modules,
        'total_lessons': total_lessons,
        'completed_lessons': total_done,
        'percent': (total_done * 100 // total_lessons) if total_lessons else 0,
    }
