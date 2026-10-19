from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    verification_url = serializers.CharField(read_only=True)
    pdf_url = serializers.SerializerMethodField()
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = [
            'id',
            'certificate_code',
            'student_name',
            'course_title',
            'issued_at',
            'is_valid',
            'verification_url',
            'pdf_url',
            'qr_code_url',
        ]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_pdf_url(self, obj):
        return obj.pdf_file.url if obj.pdf_file else None

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_qr_code_url(self, obj):
        return obj.qr_code_file.url if obj.qr_code_file else None

