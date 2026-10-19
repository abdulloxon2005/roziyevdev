import io
import os
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
import qrcode
from PIL import Image

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from apps.learning.models import Enrollment
from .models import Certificate


def generate_qr_code_image(text: str) -> BytesIO:
    """Berilgan matn/URL uchun QR-kod rasmini xotirada yaratadi."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=6,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0f172a", back_color="#ffffff")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer


def create_or_get_certificate(enrollment: Enrollment) -> Certificate:
    """
    Tugatilgan a'zolik uchun sertifikat obyektini oladi yoki yaratadi,
    PDF va QR-kodni avtomatik generatsiya qiladi.
    """
    certificate, created = Certificate.objects.get_or_create(
        enrollment=enrollment,
        defaults={
            'user': enrollment.user,
            'course': enrollment.course,
            'student_name': enrollment.user.display_name or enrollment.user.email,
            'course_title': enrollment.course.title,
            'issued_at': enrollment.completed_at or timezone.now(),
        }
    )

    # Agar PDF allaqachon mavjud bo'lsa va qayta yaratish shart bo'lmasa
    if certificate.pdf_file and not created:
        return certificate

    # 1. QR kod yaratish
    qr_buffer = generate_qr_code_image(certificate.verification_url)
    qr_filename = f"qr_{certificate.certificate_code}.png"
    certificate.qr_code_file.save(qr_filename, ContentFile(qr_buffer.getvalue()), save=False)

    # 2. PDF generatsiya qilish
    pdf_buffer = BytesIO()
    page_width, page_height = landscape(A4)
    p = canvas.Canvas(pdf_buffer, pagesize=landscape(A4))

    # Ranglar
    bg_color = colors.HexColor('#F8FAFC')
    border_outer = colors.HexColor('#0F172A')
    border_inner = colors.HexColor('#2563EB')
    gold_accent = colors.HexColor('#D97706')
    text_dark = colors.HexColor('#0F172A')
    text_muted = colors.HexColor('#64748B')
    blue_brand = colors.HexColor('#1D4ED8')

    # Fon to'ldirish
    p.setFillColor(bg_color)
    p.rect(0, 0, page_width, page_height, fill=1, stroke=0)

    # Bezakli hoshiyalar (Borders)
    # Tashqi qalin hoshiya
    p.setStrokeColor(border_outer)
    p.setLineWidth(4)
    p.rect(20, 20, page_width - 40, page_height - 40)

    # Ichki nafis oltin/ko'k hoshiya
    p.setStrokeColor(gold_accent)
    p.setLineWidth(1.5)
    p.rect(26, 26, page_width - 52, page_height - 52)

    # Burchak bezaklari
    corner_size = 20
    p.setFillColor(gold_accent)
    # Yuqori-chap
    p.rect(26, page_height - 26 - corner_size, corner_size, corner_size, fill=1, stroke=0)
    # Yuqori-o'ng
    p.rect(page_width - 26 - corner_size, page_height - 26 - corner_size, corner_size, corner_size, fill=1, stroke=0)
    # Quyi-chap
    p.rect(26, 26, corner_size, corner_size, fill=1, stroke=0)
    # Quyi-o'ng
    p.rect(page_width - 26 - corner_size, 26, corner_size, corner_size, fill=1, stroke=0)

    # Logo joylash
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo_emblem.png')
    if os.path.exists(logo_path):
        p.drawImage(logo_path, page_width / 2 - 30, page_height - 110, width=60, height=56, preserveAspectRatio=True, mask='auto')

    # Sarlavha: RoziyevDev Academy
    p.setFillColor(border_outer)
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(page_width / 2, page_height - 130, "ROZIYEVDEV ONLINE ACADEMY")

    p.setFillColor(gold_accent)
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(page_width / 2, page_height - 146, "ZAMONAVIY AXBOROT TEXNOLOGIYALARI MAKTABI")

    # Katta sertifikat sarlavhasi
    p.setFillColor(blue_brand)
    p.setFont("Helvetica-Bold", 30)
    p.drawCentredString(page_width / 2, page_height - 190, "SERTIFIKAT")

    p.setFillColor(text_muted)
    p.setFont("Helvetica", 11)
    p.drawCentredString(page_width / 2, page_height - 212, "Ushbu sertifikat egasi quyidagi dasturlash kursini muvaffaqiyatli tamomladi:")

    # Talaba ismi
    p.setFillColor(text_dark)
    p.setFont("Helvetica-Bold", 26)
    p.drawCentredString(page_width / 2, page_height - 260, certificate.student_name)

    # Chiziq
    p.setStrokeColor(colors.HexColor('#CBD5E1'))
    p.setLineWidth(1)
    p.line(page_width / 2 - 180, page_height - 275, page_width / 2 + 180, page_height - 275)

    # Kurs nomi
    p.setFillColor(blue_brand)
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(page_width / 2, page_height - 315, f"«{certificate.course_title}»")

    p.setFillColor(text_muted)
    p.setFont("Helvetica", 10)
    issued_date_str = certificate.issued_at.strftime('%d.%m.%Y')
    p.drawCentredString(page_width / 2, page_height - 340, f"Berilgan sana: {issued_date_str}   |   Sertifikat ID: {certificate.certificate_code}")

    # Pastki qism: Muallif imzosi va QR kod
    # Chap tomon: Imzo
    sig_x = 100
    p.setStrokeColor(colors.HexColor('#64748B'))
    p.setLineWidth(1)
    p.line(sig_x, 90, sig_x + 180, 90)

    p.setFillColor(text_dark)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(sig_x, 72, "Abdulaziz Roziyev")
    p.setFillColor(text_muted)
    p.setFont("Helvetica", 9)
    p.drawString(sig_x, 58, "Platforma asoschisi & Bosh o'qituvchi")

    # Markaz: Tasdiq muhr belgisi
    p.setFillColor(colors.HexColor('#10B981'))
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(page_width / 2, 75, "✓ RASMIY ELEKTRON TASDIQLANGAN")
    p.setFillColor(text_muted)
    p.setFont("Helvetica", 8)
    p.drawCentredString(page_width / 2, 60, "roziyevdev.uz orqali haqiqiyligi kafolatlangan")

    # O'ng tomon: QR Kod
    qr_x = page_width - 200
    qr_y = 45
    qr_buffer.seek(0)
    # Temporary draw image from stream
    from reportlab.lib.utils import ImageReader
    qr_img = ImageReader(qr_buffer)
    p.drawImage(qr_img, qr_x, qr_y, width=70, height=70, preserveAspectRatio=True)

    p.setFillColor(text_muted)
    p.setFont("Helvetica", 8)
    p.drawString(qr_x + 78, qr_y + 45, "Haqiqiyligini tekshirish:")
    p.setFillColor(blue_brand)
    p.setFont("Helvetica", 7)
    p.drawString(qr_x + 78, qr_y + 30, "QR kodni skanerlang")
    p.drawString(qr_x + 78, qr_y + 18, f"kod: {certificate.certificate_code}")

    p.showPage()
    p.save()

    pdf_buffer.seek(0)
    pdf_filename = f"cert_{certificate.certificate_code}.pdf"
    certificate.pdf_file.save(pdf_filename, ContentFile(pdf_buffer.getvalue()), save=True)

    return certificate
