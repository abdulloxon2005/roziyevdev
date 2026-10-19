"""
URL Configuration for roziyevdev project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from apps.core.views import web_home_view, HealthCheckAPIView
from apps.courses.views import web_course_list_view, web_course_detail_view
from apps.users.views import (
    web_login_view,
    web_register_view,
    web_logout_view,
    web_profile_view,
    web_profile_settings_view,
    web_quick_unlock_view,
)


def staff_only_hidden(view):
    """API hujjatlarini faqat tizimga kirgan adminlarga ko'rsatadi.
    Boshqalar uchun sahifa umuman mavjud emasdek 404 qaytariladi."""
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not (user.is_authenticated and (user.is_staff or user.is_superuser)):
            raise Http404()
        return view(request, *args, **kwargs)
    return _wrapped


urlpatterns = [
    # Django Admin paneli
    path('admin/', admin.site.urls),

    # =========================================================================
    # REST API Hujjatlashtirish (faqat adminlar uchun, boshqalarga yashirin)
    # =========================================================================
    path('api/schema/', staff_only_hidden(SpectacularAPIView.as_view()), name='schema'),
    path('api/docs/', staff_only_hidden(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    path('api/redoc/', staff_only_hidden(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),

    # =========================================================================
    # REST API Endpoints (/api/v1/...)
    # =========================================================================
    path('api/v1/health/', HealthCheckAPIView.as_view(), name='api_health'),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/courses/', include('apps.courses.urls')),
    path('api/v1/learning/', include('apps.learning.api_urls')),
    path('api/v1/blog/', include('apps.blog.api_urls')),
    path('api/v1/orders/', include('apps.orders.api_urls')),
    path('api/v1/certificates/', include('apps.certificates.api_urls')),

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
    path('auth/quick-unlock/', web_quick_unlock_view, name='quick_unlock'),
    path('profile/', web_profile_view, name='profile'),
    path('profile/settings/', web_profile_settings_view, name='profile_settings'),

    # Ustoz Studiyasi / Admin Paneli (Dashboard)
    path('dashboard/', include('apps.dashboard.urls')),

    # O'quvchi Paneli (Student Portal: Vazifalar, Reyting, Musobaqalar, Loyihalar, Roadmap)
    path('student/', include('apps.student.urls')),

    # O'quv jarayoni (Learning)
    path('', include('apps.learning.urls')),

    # Shaxsiy IT Blog
    path('blog/', include('apps.blog.urls')),

    # Buyurtmalar va To'lovlar (Orders)
    path('orders/', include('apps.orders.urls')),

    # Sertifikatlar (Certificates)
    path('certificates/', include('apps.certificates.urls')),
]

# Rasm va media fayllarni ko'rsatish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
