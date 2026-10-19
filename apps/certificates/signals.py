import logging
from django.dispatch import receiver
from apps.learning.signals import course_completed
from .services import create_or_get_certificate

logger = logging.getLogger(__name__)


@receiver(course_completed)
def handle_course_completed(sender, enrollment, **kwargs):
    """Talaba kursni 100% tugatganda avtomatik sertifikat yaratish."""
    try:
        certificate = create_or_get_certificate(enrollment)
        logger.info(f"Sertifikat muvaffaqiyatli yaratildi: {certificate.certificate_code} ({enrollment.user.email})")
    except Exception as e:
        logger.error(f"Sertifikat yaratishda xatolik: {e}", exc_info=True)
