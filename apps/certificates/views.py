from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Certificate
from .serializers import CertificateSerializer


# ==============================================================================
# WEB VIEWS
# ==============================================================================

def web_certificate_verify_view(request, code):
    """Ommaviy sertifikat tekshirish sahifasi (QR kod orqali o'tiladigan sahifa)."""
    certificate = get_object_or_404(Certificate, certificate_code=code)
    context = {
        'certificate': certificate,
        'course': certificate.course,
        'user_obj': certificate.user,
    }
    return render(request, 'certificates/verify.html', context)


def web_certificate_download_view(request, code):
    """Sertifikat PDF faylini to'g'ridan-to'g'ri yuklab olish."""
    certificate = get_object_or_404(Certificate, certificate_code=code)
    if not certificate.pdf_file:
        raise Http404("Sertifikat PDF fayli topilmadi.")
    response = FileResponse(certificate.pdf_file.open('rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="sertifikat_{certificate.certificate_code}.pdf"'
    return response


@login_required
def web_my_certificates_view(request):
    """Foydalanuvchining o'z sertifikatlari ro'yxati."""
    certificates = Certificate.objects.filter(user=request.user).select_related('course')
    context = {
        'certificates': certificates,
        'active_menu': 'certificates',
    }
    return render(request, 'certificates/list.html', context)


# ==============================================================================
# REST API VIEWS
# ==============================================================================

class CertificateVerifyAPIView(APIView):
    """Sertifikat kodini tekshirish API'si."""
    permission_classes = [permissions.AllowAny]

    @extend_schema(responses={200: CertificateSerializer})
    def get(self, request, code):
        certificate = get_object_or_404(Certificate, certificate_code=code)
        serializer = CertificateSerializer(certificate)
        return Response(serializer.data)


class MyCertificatesAPIView(APIView):
    """Talabaning barcha qo'lga kiritgan sertifikatlari."""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: CertificateSerializer(many=True)})
    def get(self, request):
        certificates = Certificate.objects.filter(user=request.user).select_related('course')
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)
