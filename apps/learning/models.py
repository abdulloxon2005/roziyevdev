from django.db import models, transaction
from django.utils import timezone

from apps.core.models import TimeStampedModel
from apps.courses.models import Course, Lesson
from apps.users.models import CustomUser


class Enrollment(TimeStampedModel):
    """Foydalanuvchining kursga a'zoligi va umumiy progressi."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Talaba")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Kurs")
    progress_percent = models.PositiveSmallIntegerField(default=0, verbose_name="Progress (%)")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Tugatilgan vaqt")
    last_lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, null=True, blank=True, related_name='+', verbose_name="Oxirgi dars"
    )

    class Meta:
        verbose_name = "Kursga a'zolik"
        verbose_name_plural = "Kursga a'zoliklar"
        ordering = ['-updated_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'course'], name='unique_enrollment_per_user_course'),
        ]

    def __str__(self):
        return f"{self.user.email} → {self.course.title} ({self.progress_percent}%)"

    @property
    def is_completed(self):
        return self.completed_at is not None


class LessonProgress(TimeStampedModel):
    """Talaba tugatgan darslar."""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress_records')

    class Meta:
        verbose_name = 'Dars progressi'
        verbose_name_plural = 'Dars progresslari'
        constraints = [
            models.UniqueConstraint(fields=['enrollment', 'lesson'], name='unique_lesson_progress'),
        ]

    def __str__(self):
        return f"{self.enrollment.user.email}: {self.lesson.title}"


# ==============================================================================
# VAZIFALAR, BLOK-SXEMA VA TANGACHALAR MODELLARI
# ==============================================================================

class Assignment(TimeStampedModel):
    """Har bir darsga biriktirilgan amaliy vazifa."""
    lesson = models.OneToOneField(
        Lesson,
        on_delete=models.CASCADE,
        related_name='assignment',
        verbose_name="Dars"
    )
    title = models.CharField(max_length=250, verbose_name="Vazifa nomi")
    description = models.TextField(verbose_name="Vazifa sharti va qo'llanma (Markdown)")
    starter_code = models.TextField(blank=True, verbose_name="Boshlang'ich kod shabloni")
    coin_reward = models.PositiveIntegerField(
        default=50,
        verbose_name="Mukofot tangachalari (Coins)",
        help_text="Vazifa qabul qilinganda talabaga beriladigan tangalar soni"
    )
    max_score = models.PositiveSmallIntegerField(default=100, verbose_name="Maksimal ball")
    passing_score = models.PositiveSmallIntegerField(default=70, verbose_name="O'tish bali")
    allow_code = models.BooleanField(default=True, verbose_name="Kod orqali topshirish yoqilgan")
    allow_flowchart = models.BooleanField(default=True, verbose_name="Blok-sxema orqali topshirish yoqilgan")
    allow_file_upload = models.BooleanField(default=True, verbose_name="Fayl yuklash orqali topshirish yoqilgan")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        verbose_name = 'Vazifa'
        verbose_name_plural = 'Vazifalar'
        ordering = ['lesson__module__order', 'lesson__order']

    def __str__(self):
        return f"{self.lesson.module.course.title} | {self.lesson.title}: {self.title}"


class SubmissionStatus(models.TextChoices):
    PENDING = 'pending', 'Kutilmoqda (Tekshirilmoqda)'
    APPROVED = 'approved', 'Qabul qilindi'
    REJECTED = 'rejected', 'Qayta ishlashga qaytarildi'


class AssignmentSubmission(TimeStampedModel):
    """Talaba tomonidan yuborilgan vazifa yechimi."""
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name="Vazifa"
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='assignment_submissions',
        verbose_name="Talaba"
    )
    submitted_code = models.TextField(blank=True, verbose_name="Topshirilgan kod")
    flowchart_data = models.TextField(blank=True, verbose_name="Blok-sxema ma'lumotlari (Mermaid/JSON)")
    attached_file = models.FileField(
        upload_to='submissions/%Y/%m/',
        blank=True,
        null=True,
        verbose_name="Biriktirilgan fayl (.zip, .pdf, .dart)"
    )
    status = models.CharField(
        max_length=20,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.PENDING,
        verbose_name="Holati"
    )
    score = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Qo'yilgan ball (0-100)")
    instructor_feedback = models.TextField(blank=True, verbose_name="O'qituvchi taqrizi va izohi")
    coins_awarded = models.PositiveIntegerField(default=0, verbose_name="Berilgan tangalar")
    reviewed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_submissions',
        verbose_name="Tekshirgan o'qituvchi"
    )
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name="Tekshirilgan vaqt")

    class Meta:
        verbose_name = 'Topshirilgan vazifa'
        verbose_name_plural = 'Topshirilgan vazifalar'
        unique_together = ('assignment', 'student')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.email} -> {self.assignment.title} ({self.get_status_display()})"

    @transaction.atomic
    def approve(self, reviewer, score: int, feedback: str = ""):
        """Admin tomonidan vazifani qabul qilish, tangachalarni berish va darsni tugallash."""
        self.status = SubmissionStatus.APPROVED
        self.score = score
        self.instructor_feedback = feedback
        self.reviewed_by = reviewer
        self.reviewed_at = timezone.now()

        # Agar o'tish baliga yetsa va tangalar hali berilmagan bo'lsa
        if score >= self.assignment.passing_score and self.coins_awarded == 0:
            reward = self.assignment.coin_reward
            self.coins_awarded = reward
            self.student.add_coins(reward)
            CoinTransaction.objects.create(
                student=self.student,
                submission=self,
                amount=reward,
                description=f"«{self.assignment.title}» vazifasi uchun mukofot tangachalari"
            )

        # Vazifa muvaffaqiyatli qabul qilinganda darsni avtomatik tugallangan deb belgilash
        if score >= self.assignment.passing_score:
            from .models import Enrollment
            from .services import mark_lesson_complete
            course = self.assignment.lesson.module.course
            enrollment = Enrollment.objects.filter(user=self.student, course=course).first()
            if enrollment:
                mark_lesson_complete(enrollment, self.assignment.lesson)

        self.save(update_fields=[
            'status', 'score', 'instructor_feedback',
            'coins_awarded', 'reviewed_by', 'reviewed_at', 'updated_at'
        ])

    @transaction.atomic
    def reject(self, reviewer, feedback: str, score: int = None):
        """Admin tomonidan vazifani qayta ishlashga qaytarish va agar avval berilgan bo'lsa, tangalarni bekor qilish."""
        self.status = SubmissionStatus.REJECTED
        self.instructor_feedback = feedback
        if score is not None:
            self.score = score
        self.reviewed_by = reviewer
        self.reviewed_at = timezone.now()

        # Agar avval tangalar berilgan bo'lsa, ularni qaytarib olamiz
        if self.coins_awarded > 0:
            revoked_coins = self.coins_awarded
            self.student.add_coins(-revoked_coins)
            CoinTransaction.objects.create(
                student=self.student,
                submission=self,
                amount=-revoked_coins,
                description=f"«{self.assignment.title}» vazifasi qaytarilganligi sababli tangalar bekor qilindi"
            )
            self.coins_awarded = 0

        self.save(update_fields=[
            'status', 'score', 'instructor_feedback',
            'coins_awarded', 'reviewed_by', 'reviewed_at', 'updated_at'
        ])


class CoinTransaction(TimeStampedModel):
    """Talabaning tangachalar kirim-chiqim jurnali."""
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='coin_transactions',
        verbose_name="Talaba"
    )
    submission = models.ForeignKey(
        AssignmentSubmission,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coin_transactions',
        verbose_name="Topshiriq"
    )
    amount = models.IntegerField(verbose_name="Tangalar miqdori (+ yoki -)")
    description = models.CharField(max_length=255, verbose_name="Izoh / Manba")

    class Meta:
        verbose_name = 'Tangalar amali'
        verbose_name_plural = 'Tangalar jurnali'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.email}: {self.amount:+d} ({self.description})"
