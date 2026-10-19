"""
Django settings for roziyevdev project.

Barcha maxfiy va muhitga bog'liq qiymatlar .env fayli / muhit o'zgaruvchilaridan o'qiladi.
Namuna uchun: .env.example
"""

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


def env_bool(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in ('1', 'true', 'yes', 'on')


def env_list(name, default=''):
    return [item.strip() for item in os.getenv(name, default).split(',') if item.strip()]


# ==============================================================================
# ASOSIY XAVFSIZLIK SOZLAMALARI
DEBUG = env_bool('DJANGO_DEBUG', False)
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-prod-safe-secret-key-roziyevdev-platform-secure-token-50-chars')
if not DEBUG and SECRET_KEY.startswith('django-insecure'):
    SECRET_KEY = 'django-prod-safe-secret-key-roziyevdev-platform-secure-token-50-chars'

ALLOWED_HOSTS = env_list('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost')
CSRF_TRUSTED_ORIGINS = env_list('DJANGO_CSRF_TRUSTED_ORIGINS')
SITE_URL = os.getenv('SITE_URL', 'http://127.0.0.1:8000').rstrip('/')
# Nginx ortida ishlaganda haqiqiy IP manzilni X-Real-IP sarlavhasidan olish
USE_X_REAL_IP = env_bool('USE_X_REAL_IP', False)

# ==============================================================================
# ILOVALAR
# ==============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.humanize',

    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',

    # Loyiha modullari
    'apps.core',
    'apps.users',
    'apps.courses',
    'apps.learning',
    'apps.blog',
    'apps.orders',
    'apps.certificates',
    'apps.dashboard',
    'apps.contests',
    'apps.projects',
    'apps.roadmaps',
    'apps.student',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'apps.core.middleware.SessionIdleTimeoutMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ==============================================================================
# MA'LUMOTLAR BAZASI (DATABASE_URL orqali PostgreSQL, aks holda SQLite)
# ==============================================================================
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_USER_MODEL = 'users.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
]

# ==============================================================================
# KESH (REDIS_URL bo'lsa Redis, aks holda xotira)
# ==============================================================================
REDIS_URL = os.getenv('REDIS_URL')
if REDIS_URL:
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.redis.RedisCache', 'LOCATION': REDIS_URL}}
else:
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

# ==============================================================================
# TIL VA VAQT
# ==============================================================================
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIK VA MEDIA FAYLLAR
# ==============================================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {
        'BACKEND': (
            'django.contrib.staticfiles.storage.StaticFilesStorage'
            if DEBUG else 'whitenoise.storage.CompressedStaticFilesStorage'
        ),
    },
}

# Maksimal yuklash hajmi (Video darslar va materiallar uchun 500MB gacha ruxsat)
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv('DATA_UPLOAD_MAX_MEMORY_SIZE', 500 * 1024 * 1024))
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv('FILE_UPLOAD_MAX_MEMORY_SIZE', 50 * 1024 * 1024))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# REST FRAMEWORK
# ==============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Brauzerda interaktiv API sahifasi ko'rinmasligi uchun faqat JSON
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': os.getenv('THROTTLE_ANON', '300/hour'),
        'user': os.getenv('THROTTLE_USER', '3000/hour'),
        'auth': os.getenv('THROTTLE_AUTH', '10/minute'),
        'comments': os.getenv('THROTTLE_COMMENTS', '10/minute'),
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'RoziyevDev LMS & IT Blog API',
    'DESCRIPTION': "Online kurslar, darslar, blog, to'lovlar va sertifikatlar platformasi API hujjatlari.",
    'VERSION': '2.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# ==============================================================================
# CORS, AUTENTIFIKATSIYA YO'NALISHLARI
# ==============================================================================
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = env_list('CORS_ALLOWED_ORIGINS')
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/student/'
LOGOUT_REDIRECT_URL = '/'

# Harakatsizlik taymeri (soniyalarda): default 15 daqiqa (900 soniya)
SESSION_IDLE_TIMEOUT = int(os.getenv('SESSION_IDLE_TIMEOUT', 15 * 60))
# Agar True bo'lsa, ro'yxatdan o'tmagan mehmonlar uchun ham butun sayt yopiladi (login talab qilinadi)
LOGIN_REQUIRED_FOR_ALL = env_bool('LOGIN_REQUIRED_FOR_ALL', False)
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 86400 * 7  # 7 kunlik umumiy seans muddati

# ==============================================================================
# EMAIL
# ==============================================================================
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'RoziyevDev <no-reply@roziyev.dev>')
if os.getenv('EMAIL_HOST'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', True)
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ==============================================================================
# TELEGRAM BILDIRISHNOMALARI (ixtiyoriy)
# ==============================================================================
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID', '')

# ==============================================================================
# TO'LOV TIZIMLARI
# ==============================================================================
PAYME_MERCHANT_ID = os.getenv('PAYME_MERCHANT_ID', '')
PAYME_SECRET_KEY = os.getenv('PAYME_SECRET_KEY', '')
PAYME_TEST_MODE = env_bool('PAYME_TEST_MODE', True)
PAYME_ACCOUNT_FIELD = 'order_id'

CLICK_SERVICE_ID = os.getenv('CLICK_SERVICE_ID', '')
CLICK_MERCHANT_ID = os.getenv('CLICK_MERCHANT_ID', '')
CLICK_SECRET_KEY = os.getenv('CLICK_SECRET_KEY', '')
CLICK_MERCHANT_USER_ID = os.getenv('CLICK_MERCHANT_USER_ID', '')

# Faqat ishlab chiqish uchun: haqiqiy pulsiz "test to'lov"
PAYMENTS_DEMO_ENABLED = env_bool('PAYMENTS_DEMO_ENABLED', DEBUG)

# ==============================================================================
# PRODUCTION XAVFSIZLIGI
# ==============================================================================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = env_bool('DJANGO_SECURE_SSL_REDIRECT', False)
    SESSION_COOKIE_SECURE = env_bool('DJANGO_SECURE_COOKIES', True)
    CSRF_COOKIE_SECURE = env_bool('DJANGO_SECURE_COOKIES', True)
    SECURE_HSTS_SECONDS = int(os.getenv('DJANGO_HSTS_SECONDS', '0'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    X_FRAME_OPTIONS = os.getenv('DJANGO_X_FRAME_OPTIONS', 'SAMEORIGIN')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': os.getenv('LOG_LEVEL', 'INFO')},
}
