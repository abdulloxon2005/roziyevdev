from django.db.models import Sum, Count, Q
from django.utils import timezone
from apps.courses.models import Course, Lesson
from apps.learning.models import Enrollment, LessonProgress, Assignment, AssignmentSubmission, SubmissionStatus
from apps.projects.models import Project, ProjectStatus


def get_student_overview_stats(user):
    """O'quvchi boshqaruv paneli uchun umumiy statistikalar va tezkor ma'lumotlar."""
    enrollments = Enrollment.objects.filter(user=user).select_related('course', 'course__category', 'last_lesson').order_by('-updated_at')
    enrolled_courses_count = enrollments.count()
    completed_lessons_count = LessonProgress.objects.filter(enrollment__user=user).count()

    submissions = AssignmentSubmission.objects.filter(student=user)
    approved_submissions_count = submissions.filter(status=SubmissionStatus.APPROVED).count()
    pending_submissions_count = submissions.filter(status=SubmissionStatus.PENDING).count()
    rejected_submissions_count = submissions.filter(status=SubmissionStatus.REJECTED).count()

    # Loyihalar
    my_projects_count = Project.objects.filter(author=user).count()

    return {
        'enrollments': enrollments,
        'enrolled_courses_count': enrolled_courses_count,
        'completed_lessons_count': completed_lessons_count,
        'approved_submissions_count': approved_submissions_count,
        'pending_submissions_count': pending_submissions_count,
        'rejected_submissions_count': rejected_submissions_count,
        'coins': user.coins,
        'my_projects_count': my_projects_count,
    }
