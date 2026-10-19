from django.urls import path
from .views import (
    web_certificate_verify_view,
    web_certificate_download_view,
    web_my_certificates_view,
)

urlpatterns = [
    # Web sahifalar
    path('verify/<str:code>/', web_certificate_verify_view, name='certificate_verify'),
    path('download/<str:code>/', web_certificate_download_view, name='certificate_download'),
    path('my/', web_my_certificates_view, name='my_certificates'),
]
