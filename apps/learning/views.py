from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from django.db.models import Sum
from apps.courses.models import Course, Lesson
from .models import (
    Enrollment,
    LessonProgress,
    Assignment,
    AssignmentSubmission,
    SubmissionStatus,
    CoinTransaction,
)
from .services import (
    get_course_lessons,
    get_enrollment,
    has_full_access,
    can_access_lesson,
    enroll_user,
    mark_lesson_complete,
    mark_lesson_incomplete,
)
from .serializers import (
    EnrollmentSerializer,
    LessonLearningSerializer,
)


# ==============================================================================
# REST API
# ==============================================================================

class MyEnrollmentsAPIView(APIView):
    """Foydalanuvchining barcha yozilgan kurslari va ulardagi progressi."""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: EnrollmentSerializer(many=True)})
    def get(self, request):
        enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)


class EnrollCourseAPIView(APIView):
    """Bepul kursga yozilish API (pullik kurslar /api/v1/orders/ orqali sotib olinadi)."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnrollmentSerializer

    @extend_schema(request=None, responses={200: EnrollmentSerializer, 201: EnrollmentSerializer})
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug, is_published=True)
        if course.is_paid:
            return Response(
                {"detail": "Ushbu kurs pullik. To'lov orqali yozilishingiz mumkin."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        enrollment, created = enroll_user(request.user, course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class ToggleLessonAPIView(APIView):
    """Darsni tugatilgan/tugatilmagan deb belgilash API'si."""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=None, responses={200: dict})
    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson.objects.select_related('module__course'), id=lesson_id)
        enrollment = get_enrollment(request.user, lesson.module.course)
        if not enrollment:
            return Response({"detail": "Avval kursga yozilishingiz kerak."}, status=status.HTTP_403_FORBIDDEN)

        is_completed = LessonProgress.objects.filter(enrollment=enrollment, lesson=lesson).exists()
        if is_completed:
            mark_lesson_incomplete(enrollment, lesson)
            completed_now = False
        else:
            mark_lesson_complete(enrollment, lesson)
            completed_now = True

        enrollment.refresh_from_db()
        return Response({
            "lesson_id": lesson.id,
            "is_completed": completed_now,
            "progress_percent": enrollment.progress_percent,
            "course_completed": enrollment.is_completed,
        })


# ==============================================================================
# WEB VIEWS
# ==============================================================================

@login_required
def web_enroll_action_view(request, slug):
    """Kursga a'zo bo'lish harakati: bepul bo'lsa darhol yoziladi, pullik bo'lsa checkout sahifasiga yuboradi."""
    course = get_object_or_404(Course, slug=slug, is_published=True)
    if course.is_paid:
        return redirect('order_checkout', slug=course.slug)

    enrollment, created = enroll_user(request.user, course)
    if created:
        messages.success(request, f"Tabriklaymiz! Siz '{course.title}' kursiga muvaffaqiyatli yozildingiz.")
    return redirect('course_learn', slug=course.slug)


def web_course_learn_view(request, slug, lesson_id=None):
    """
    Onlayn dars xonasi: video pleer, dars matni, yuklanmalar,
    modullar mundarijasi va progress paneli.
    """
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment = get_enrollment(request.user, course) if request.user.is_authenticated else None
    has_access = has_full_access(request.user, course, enrollment)

    # Kursning barcha darslari tartiblangan holda
    all_lessons = get_course_lessons(course)
    if not all_lessons:
        messages.info(request, "Ushbu kursda darslar tez orada yuklanadi.")
        return redirect('course_detail', slug=course.slug)

    # Tanlangan darsni aniqlash
    current_lesson = None
    if lesson_id:
        current_lesson = next((l for l in all_lessons if l.id == lesson_id), None)
    if not current_lesson:
        if enrollment and enrollment.last_lesson_id:
            current_lesson = next((l for l in all_lessons if l.id == enrollment.last_lesson_id), None)
        if not current_lesson:
            current_lesson = all_lessons[0]

    # Ruxsatni tekshirish
    can_view = can_access_lesson(request.user, current_lesson, enrollment)

    # Keyingi va oldingi darslar
    current_index = all_lessons.index(current_lesson) if current_lesson in all_lessons else 0
    prev_lesson = all_lessons[current_index - 1] if current_index > 0 else None
    next_lesson = all_lessons[current_index + 1] if current_index < len(all_lessons) - 1 else None

    # Tugatilgan darslar to'plami
    completed_lesson_ids = set()
    if enrollment:
        completed_lesson_ids = set(
            LessonProgress.objects.filter(enrollment=enrollment).values_list('lesson_id', flat=True)
        )

    # Modullarni darslari bilan birga tayyorlash
    modules_with_lessons = []
    for module in course.modules.all().prefetch_related('lessons'):
        mod_lessons = [l for l in all_lessons if l.module_id == module.id]
        modules_with_lessons.append({
            'module': module,
            'lessons': mod_lessons,
        })

    # Darsga biriktirilgan amaliy vazifa va foydalanuvchi topshirig'i
    from .models import Assignment, AssignmentSubmission, SubmissionStatus
    assignment = getattr(current_lesson, 'assignment', None)
    if assignment and not assignment.is_active:
        assignment = None
    if not assignment and current_lesson:
        assignment = Assignment.objects.filter(lesson=current_lesson, is_active=True).first()

    user_submission = None
    if assignment and request.user.is_authenticated:
        user_submission = AssignmentSubmission.objects.filter(
            assignment=assignment,
            student=request.user
        ).order_by('-created_at').first()

    context = {
        'course': course,
        'enrollment': enrollment,
        'has_access': has_access,
        'current_lesson': current_lesson,
        'can_view': can_view,
        'prev_lesson': prev_lesson,
        'next_lesson': next_lesson,
        'completed_lesson_ids': completed_lesson_ids,
        'modules_with_lessons': modules_with_lessons,
        'total_lessons': len(all_lessons),
        'assignment': assignment,
        'user_submission': user_submission,
    }
    return render(request, 'learning/player.html', context)


@login_required
@require_POST
def web_submit_assignment_view(request, assignment_id):
    """Talaba tomonidan dars vazifasini topshirish."""
    import os
    from .models import Assignment, AssignmentSubmission, SubmissionStatus
    assignment = get_object_or_404(
        Assignment.objects.select_related('lesson__module__course'),
        id=assignment_id,
        is_active=True
    )
    course = assignment.lesson.module.course
    enrollment = get_enrollment(request.user, course)
    if not has_full_access(request.user, course, enrollment):
        messages.error(request, "Vazifani topshirish uchun kursga a'zo bo'lishingiz kerak.")
        return redirect('course_detail', slug=course.slug)

    # Qabul qilingan vazifani qayta yuborishni bloklash
    existing_sub = AssignmentSubmission.objects.filter(assignment=assignment, student=request.user).first()
    if existing_sub and existing_sub.status == SubmissionStatus.APPROVED:
        messages.info(request, "Ushbu vazifangiz allaqachon muvaffaqiyatli qabul qilingan va baholangan.")
        return redirect('course_learn_lesson', slug=course.slug, lesson_id=assignment.lesson.id)

    submitted_code = request.POST.get('submitted_code', '').strip()
    flowchart_data = request.POST.get('flowchart_data', '').strip()
    attached_file = request.FILES.get('attached_file')

    # Fayl xavfsizligi va hajmini tekshirish
    if attached_file:
        max_size = 25 * 1024 * 1024  # 25 MB
        allowed_extensions = {'.zip', '.rar', '.pdf', '.dart', '.py', '.sql', '.txt', '.docx', '.png', '.jpg', '.jpeg'}
        if attached_file.size > max_size:
            messages.error(request, "Yuklangan fayl hajmi 25 MB dan oshmasligi kerak.")
            return redirect('course_learn_lesson', slug=course.slug, lesson_id=assignment.lesson.id)

        ext = os.path.splitext(attached_file.name)[1].lower()
        if ext not in allowed_extensions:
            messages.error(request, f"«{ext}» formati ruxsat etilmagan. Faqat arxiv (.zip), kod yoki hujjat fayllarini yuklang.")
            return redirect('course_learn_lesson', slug=course.slug, lesson_id=assignment.lesson.id)

    if not submitted_code and not flowchart_data and not attached_file:
        messages.error(request, "Iltimos, kod yozing, blok-sxema chizing yoki fayl biriktiring.")
        return redirect('course_learn_lesson', slug=course.slug, lesson_id=assignment.lesson.id)

    # Mavjud topshiriqni topish yoki yangi yaratish
    submission, created = AssignmentSubmission.objects.get_or_create(
        assignment=assignment,
        student=request.user,
        defaults={
            'submitted_code': submitted_code,
            'flowchart_data': flowchart_data,
            'attached_file': attached_file,
            'status': SubmissionStatus.PENDING,
        }
    )

    if not created:
        if submitted_code:
            submission.submitted_code = submitted_code
        if flowchart_data:
            submission.flowchart_data = flowchart_data
        if attached_file:
            submission.attached_file = attached_file
        submission.status = SubmissionStatus.PENDING
        submission.instructor_feedback = ""
        submission.save()

    messages.success(request, "Vazifangiz muvaffaqiyatli topshirildi! O'qituvchi tez orada tekshirib ball qo'yadi.")
    return redirect('course_learn_lesson', slug=course.slug, lesson_id=assignment.lesson.id)


@login_required
@require_POST
def web_toggle_lesson_view(request, lesson_id):
    """Web interfeysdan darsni tugatilgan/tugatilmagan deb belgilash."""
    lesson = get_object_or_404(Lesson.objects.select_related('module__course'), id=lesson_id)
    enrollment = get_enrollment(request.user, lesson.module.course)
    if not enrollment:
        return JsonResponse({"error": "Kursga yozilmagan"}, status=403)

    is_completed = LessonProgress.objects.filter(enrollment=enrollment, lesson=lesson).exists()
    if is_completed:
        mark_lesson_incomplete(enrollment, lesson)
        new_state = False
    else:
        mark_lesson_complete(enrollment, lesson)
        new_state = True

    enrollment.refresh_from_db()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            "success": True,
            "is_completed": new_state,
            "progress_percent": enrollment.progress_percent,
            "is_course_completed": enrollment.is_completed,
        })

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    return redirect(next_url or 'home')


# ==============================================================================
# INSTRUCTOR REVIEW DESK (Admin Tekshiruvi)
# ==============================================================================

@login_required
def web_submissions_list_view(request):
    """O'qituvchi/Admin uchun topshirilgan vazifalar ro'yxati va filtri."""
    if not (request.user.is_staff or getattr(request.user, 'role', '') in ['instructor', 'admin'] or request.user.is_superuser):
        messages.error(request, "Ushbu sahifaga kirish huquqi faqat o'qituvchi va adminlarga berilgan.")
        return redirect('home')

    status_filter = request.GET.get('status', '').strip()
    course_filter = request.GET.get('course', '').strip()

    qs = AssignmentSubmission.objects.select_related(
        'student',
        'assignment__lesson__module__course',
        'reviewed_by'
    ).order_by('-created_at')

    if status_filter in [SubmissionStatus.PENDING, SubmissionStatus.APPROVED, SubmissionStatus.REJECTED]:
        qs = qs.filter(status=status_filter)

    if course_filter and course_filter.isdigit():
        qs = qs.filter(assignment__lesson__module__course_id=int(course_filter))

    # Statistik hisob-kitoblar
    all_subs = AssignmentSubmission.objects.all()
    pending_count = all_subs.filter(status=SubmissionStatus.PENDING).count()
    approved_count = all_subs.filter(status=SubmissionStatus.APPROVED).count()
    rejected_count = all_subs.filter(status=SubmissionStatus.REJECTED).count()
    total_coins_awarded = all_subs.aggregate(total=Sum('coins_awarded'))['total'] or 0

    courses = Course.objects.filter(is_published=True).order_by('title')

    context = {
        'submissions': qs,
        'status_filter': status_filter,
        'course_filter': course_filter,
        'courses': courses,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'total_coins_awarded': total_coins_awarded,
    }
    return render(request, 'learning/review_list.html', context)


@login_required
def web_review_submission_view(request, submission_id):
    """O'qituvchi/Admin tomonidan topshiriqni batafsil tekshirish, ball va tangalar berish."""
    if not (request.user.is_staff or getattr(request.user, 'role', '') in ['instructor', 'admin'] or request.user.is_superuser):
        messages.error(request, "Ushbu sahifaga kirish huquqi faqat o'qituvchi va adminlarga berilgan.")
        return redirect('home')

    submission = get_object_or_404(
        AssignmentSubmission.objects.select_related(
            'student__profile',
            'assignment__lesson__module__course',
            'reviewed_by'
        ),
        id=submission_id
    )

    if request.method == 'POST':
        action = request.POST.get('action')  # 'approve' or 'reject'
        score_val = request.POST.get('score', '').strip()
        feedback = request.POST.get('feedback', '').strip()

        score = int(score_val) if score_val.isdigit() else 0
        score = min(max(score, 0), submission.assignment.max_score)

        if action == 'approve':
            submission.approve(reviewer=request.user, score=score, feedback=feedback)
            messages.success(
                request,
                f"«{submission.student.display_name}»ning vazifasi qabul qilindi! {score} ball va {submission.coins_awarded} tanga berildi."
            )
        elif action == 'reject':
            submission.reject(reviewer=request.user, feedback=feedback, score=score)
            messages.warning(
                request,
                f"«{submission.student.display_name}»ning vazifasi qayta ishlash uchun qaytarildi."
            )
        return redirect('submissions_review_list')

    context = {
        'submission': submission,
        'assignment': submission.assignment,
        'course': submission.assignment.lesson.module.course,
        'lesson': submission.assignment.lesson,
    }
    return render(request, 'learning/review_detail.html', context)
