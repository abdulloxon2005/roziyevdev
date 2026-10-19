"""O'quv jarayoni biznes-mantiqi: yozilish, darsga ruxsat, progress hisoblash."""
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.courses.models import Course, Lesson

from .models import Enrollment, LessonProgress
from .signals import course_completed


def get_course_lessons(course):
    """Kursning barcha darslari to'g'ri tartibda (modul → dars)."""
    return list(
        Lesson.objects.filter(module__course=course)
        .select_related('module')
        .order_by('module__order', 'module__id', 'order', 'id')
    )


def get_enrollment(user, course):
    if not user.is_authenticated:
        return None
    return Enrollment.objects.filter(user=user, course=course).first()


def has_full_access(user, course, enrollment=None):
    """Kursning barcha darslariga ruxsat: a'zo talaba, kurs muallifi yoki admin."""
    if not user.is_authenticated:
        return False
    if user.is_staff or course.instructor_id == user.id:
        return True
    return enrollment is not None


def can_access_lesson(user, lesson, enrollment=None):
    return lesson.is_preview or has_full_access(user, lesson.module.course, enrollment)


@transaction.atomic
def enroll_user(user, course):
    enrollment, created = Enrollment.objects.get_or_create(user=user, course=course)
    if created:
        Course.objects.filter(pk=course.pk).update(students_count=F('students_count') + 1)
    return enrollment, created


def recalculate_progress(enrollment):
    """Progressni qayta hisoblaydi. Qaytaradi: kurs aynan hozir tugatildimi (True/False)."""
    total = Lesson.objects.filter(module__course_id=enrollment.course_id).count()
    done = enrollment.lesson_progress.count()
    # floor: 199/200 dars "100%" bo'lib ko'rinmasligi uchun
    enrollment.progress_percent = (done * 100 // total) if total else 0

    just_completed = False
    if total and done >= total:
        if enrollment.completed_at is None:
            enrollment.completed_at = timezone.now()
            just_completed = True
    else:
        enrollment.completed_at = None

    enrollment.save(update_fields=['progress_percent', 'completed_at', 'last_lesson', 'updated_at'])
    if just_completed:
        transaction.on_commit(lambda: course_completed.send(sender=Enrollment, enrollment=enrollment))
    return just_completed


@transaction.atomic
def mark_lesson_complete(enrollment, lesson):
    LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
    enrollment.last_lesson = lesson
    return recalculate_progress(enrollment)


@transaction.atomic
def mark_lesson_incomplete(enrollment, lesson):
    LessonProgress.objects.filter(enrollment=enrollment, lesson=lesson).delete()
    return recalculate_progress(enrollment)
