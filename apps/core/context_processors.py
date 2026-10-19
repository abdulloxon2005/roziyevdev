from django.conf import settings


def site(request):
    return {
        'SITE_NAME': 'RoziyevDev',
        'SITE_URL': settings.SITE_URL,
        'SESSION_IDLE_TIMEOUT': getattr(settings, 'SESSION_IDLE_TIMEOUT', 900),
    }
