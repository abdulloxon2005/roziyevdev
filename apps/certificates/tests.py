from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser
from apps.courses.models import Course, Category
from apps.learning.models import Enrollment
from apps.certificates.models import Certificate
from apps.certificates.services import create_or_get_certificate


class CertificatesTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="cert_student",
            email="cert_student@example.com",
            password="password123",
            first_name="Jasur",
            last_name="Karimov"
        )
        self.category = Category.objects.create(name="DB", slug="db")
        self.course = Course.objects.create(
            title="PostgreSQL Mastery",
            slug="postgresql-mastery",
            category=self.category,
            is_free=True
        )
        self.enrollment = Enrollment.objects.create(
            user=self.user,
            course=self.course,
            progress_percent=100
        )

    def test_certificate_generation(self):
        cert = create_or_get_certificate(self.enrollment)
        self.assertIsNotNone(cert)
        self.assertTrue(cert.certificate_code.startswith("ROZ-"))
        self.assertEqual(cert.student_name, "Jasur Karimov")
        self.assertTrue(bool(cert.pdf_file))
        self.assertTrue(bool(cert.qr_code_file))

    def test_certificate_verify_view(self):
        cert = create_or_get_certificate(self.enrollment)
        response = self.client.get(reverse('certificate_verify', args=[cert.certificate_code]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, cert.certificate_code)
        self.assertContains(response, "Jasur Karimov")
        self.assertContains(response, "PostgreSQL Mastery")
