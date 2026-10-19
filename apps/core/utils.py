from django.conf import settings
from django.utils.text import slugify


def unique_slugify(instance, value, slug_field='slug', max_length=200):
    """Model uchun takrorlanmas slug yaratadi (masalan: 'flutter-asoslari', 'flutter-asoslari-2')."""
    base = slugify(value)[:max_length] or 'item'
    model = instance.__class__
    queryset = model._default_manager.all()
    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    slug, counter = base, 2
    while queryset.filter(**{slug_field: slug}).exists():
        suffix = f'-{counter}'
        slug = f'{base[:max_length - len(suffix)]}{suffix}'
        counter += 1
    return slug


def get_client_ip(request):
    """
    Mijoz IP manzili. X-Real-IP faqat USE_X_REAL_IP=True bo'lsa (ya'ni Nginx ortida) ishonchli hisoblanadi,
    aks holda sarlavhani soxtalashtirib cheklovlarni chetlab o'tish mumkin bo'lardi.
    """
    if settings.USE_X_REAL_IP:
        real_ip = request.META.get('HTTP_X_REAL_IP')
        if real_ip:
            return real_ip.strip()
    return request.META.get('REMOTE_ADDR', '')
