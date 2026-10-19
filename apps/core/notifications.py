"""
Bildirishnomalar: Email va Telegram.
Ikkalasi ham xatolikda saytni to'xtatmaydi (faqat logga yoziladi).
Hozircha sinxron yuboriladi; yuklama oshganda Celery navbatiga ko'chirish tavsiya etiladi.
"""
import logging
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_email(subject, message, recipients):
    recipients = [r for r in recipients if r]
    if not recipients:
        return False
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipients, fail_silently=False)
        return True
    except Exception:  # noqa: BLE001 - bildirishnoma xatosi asosiy jarayonni buzmasligi kerak
        logger.exception("Email yuborilmadi: %s", subject)
        return False


def send_telegram(text, chat_id=None):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = chat_id or settings.TELEGRAM_CHANNEL_ID
    if not token or not chat_id:
        return False
    payload = urllib.parse.urlencode({
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
    }).encode()
    try:
        urllib.request.urlopen(f'https://api.telegram.org/bot{token}/sendMessage', data=payload, timeout=5)
        return True
    except Exception:  # noqa: BLE001
        logger.exception("Telegram xabari yuborilmadi")
        return False
