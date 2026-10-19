from django.urls import path
from .views import (
    CertificateVerifyAPIView,
    MyCertificatesAPIView,
)

urlpatterns = [
    # REST API endpoints
    path('verify/<str:code>/', CertificateVerifyAPIView.as_view(), name='api_certificate_verify'),
    path('my/', MyCertificatesAPIView.as_view(), name='api_my_certificates'),

    # Eski /api/ prefiksi bilan moslik (Backwards compatibility)
    path('api/certificates/verify/<str:code>/', CertificateVerifyAPIView.as_view()),
    path('api/certificates/my/', MyCertificatesAPIView.as_view()),
]
