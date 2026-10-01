"""
URL Configuration for roziyevdev project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from apps.core.views import web_home_view, HealthCheckAPIView
from apps.courses.views import web_course_list_view, web_course_detail_view
from apps.users.views import (
    web_login_view,
    web_register_view,
    web_logout_view,
    web_profile_view,
    web_profile_settings_view,
)

urlpatterns = [
    # Django Admin paneli
    path('admin/', admin.site.urls),

    # =========================================================================
    # REST API Hujjatlashtirish (Swagger & OpenAPI 3.0)
    # =========================================================================
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # =========================================================================
    # REST API Endpoints (/api/v1/...)
    # =========================================================================
    path('api/v1/health/', HealthCheckAPIView.as_view(), name='api_health'),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/courses/', include('apps.courses.urls')),

    # =========================================================================
    # Web UI Sahifalari (Frontend)
    # =========================================================================
    # Asosiy Sahifa
    path('', web_home_view, name='home'),

    # Kurslar sahifalari
    path('courses/', web_course_list_view, name='course_list'),
    path('courses/<slug:slug>/', web_course_detail_view, name='course_detail'),

    # Foydalanuvchi va Autentifikatsiya sahifalari
    path('auth/login/', web_login_view, name='login'),
    path('auth/register/', web_register_view, name='register'),
    path('auth/logout/', web_logout_view, name='logout'),
    path('profile/', web_profile_view, name='profile'),
    path('profile/settings/', web_profile_settings_view, name='profile_settings'),
]

# Rasm va media fayllarni ko'rsatish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
