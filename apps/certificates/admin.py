from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('certificate_code', 'student_name', 'course_title', 'issued_at', 'is_valid')
    list_filter = ('is_valid', 'issued_at')
    search_fields = ('certificate_code', 'student_name', 'course_title', 'user__email')
    readonly_fields = ('certificate_code', 'issued_at', 'created_at', 'updated_at')
    ordering = ('-issued_at',)
