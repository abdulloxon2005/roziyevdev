from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Category, Course, CourseLevel


class CoursesAPITests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Mobil Dasturlash",
            slug="mobil-dasturlash",
            icon="fa-solid fa-mobile",
            description="Mobil ilovalar yaratish",
        )
        self.course = Course.objects.create(
            title="Flutter Test Kursi",
            slug="flutter-test-kursi",
            category=self.category,
            short_description="Flutter kursi tavsifi",
            description="Batafsil ma'lumot",
            level=CourseLevel.BEGINNER,
            price=200000,
            is_free=False,
            is_published=True,
        )

    def test_category_list_api(self):
        url = reverse('api_category_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_course_list_api(self):
        url = reverse('api_course_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)

    def test_course_detail_api(self):
        url = reverse('api_course_detail', kwargs={'slug': self.course.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Flutter Test Kursi")


class CoursesWebViewsTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Algoritmlar",
            slug="algoritmlar",
            icon="fa-solid fa-code",
            description="Algoritmlar",
        )
        self.course = Course.objects.create(
            title="Algoritmlar Asoslari",
            slug="algoritmlar-asoslari",
            category=self.category,
            short_description="Qisqa ma'lumot",
            description="To'liq ma'lumot",
            level=CourseLevel.BEGINNER,
            price=0,
            is_free=True,
            is_published=True,
        )

    def test_home_page_renders(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "roziyev")
        self.assertContains(response, "Mobil Dasturlash")

    def test_courses_list_page_renders(self):
        response = self.client.get(reverse('course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algoritmlar Asoslari")

    def test_course_detail_page_renders(self):
        response = self.client.get(reverse('course_detail', kwargs={'slug': self.course.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algoritmlar Asoslari")
        self.assertContains(response, "Bepul Kurs")
