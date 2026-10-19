import uuid
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.users.models import CustomUser
from apps.courses.models import Course
from apps.learning.models import Enrollment


def generate_certificate_code():
    token = uuid.uuid4().hex[:8].upper()
    year = timezone.now().year
    return f"ROZ-{year}-{token}"


class Certificate(TimeStampedModel):
    certificate_code = models.CharField(
        max_length=40,
        unique=True,
        default=generate_certificate_code,
        verbose_name="Sertifikat kodi"
    )
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='certificate',
        verbose_name="A'zolik (Enrollment)"
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name="Talaba"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='certificates',
        verbose_name="Kurs"
    )
    student_name = models.CharField(
        max_length=200,
        verbose_name="Talaba F.I.Sh."
    )
    course_title = models.CharField(
        max_length=250,
        verbose_name="Kurs nomi"
    )
    issued_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Berilgan sana"
    )
    pdf_file = models.FileField(
        upload_to='certificates/pdfs/%Y/',
        blank=True,
        null=True,
        verbose_name="PDF fayl"
    )
    qr_code_file = models.ImageField(
        upload_to='certificates/qrs/%Y/',
        blank=True,
        null=True,
        verbose_name="QR kod rasmi"
    )
    is_valid = models.BooleanField(
        default=True,
        verbose_name="Haqiqiymi?"
    )

    class Meta:
        verbose_name = 'Sertifikat'
        verbose_name_plural = 'Sertifikatlar'
        ordering = ['-issued_at']

    def __str__(self):
        return f"{self.certificate_code} - {self.student_name} ({self.course_title})"

    def get_absolute_url(self):
        return reverse('certificate_verify', args=[self.certificate_code])

    @property
    def verification_url(self):
        base = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000').rstrip('/')
        return f"{base}/certificates/verify/{self.certificate_code}/"
