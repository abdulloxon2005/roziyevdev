from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser, Profile, UserRole


class UserAuthAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse('api_register')
        self.login_url = reverse('api_login')
        self.profile_url = reverse('api_profile_me')

        self.user_data = {
            'email': 'student_test@roziyev.dev',
            'username': 'student_test',
            'first_name': 'Ali',
            'last_name': 'Valiyev',
            'password': 'SecurePassword123!',
            'password_confirm': 'SecurePassword123!',
        }

    def test_user_registration_api(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertEqual(response.data['user']['email'], self.user_data['email'])

        # Profile auto-created check
        user = CustomUser.objects.get(email=self.user_data['email'])
        self.assertTrue(hasattr(user, 'profile'))

    def test_user_login_api(self):
        # Register user first
        CustomUser.objects.create_user(
            email='login_test@roziyev.dev',
            username='login_test',
            password='TestPassword123!',
        )

        response = self.client.post(
            self.login_url,
            {'email': 'login_test@roziyev.dev', 'password': 'TestPassword123!'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])

    def test_profile_update_api(self):
        user = CustomUser.objects.create_user(
            email='profile_test@roziyev.dev',
            username='profile_test',
            password='TestPassword123!',
        )
        self.client.force_authenticate(user=user)

        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        update_data = {
            'first_name': 'Alisher',
            'headline': 'Senior Flutter Engineer',
            'telegram': '@alisher_flutter',
        }
        update_response = self.client.put(self.profile_url, update_data, format='json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Alisher')
        self.assertEqual(user.profile.headline, 'Senior Flutter Engineer')


class UserWebViewsTests(TestCase):
    def test_login_page_renders(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tizimga Kirish")

    def test_register_page_renders(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hisob Yaratish")

    def test_profile_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_student_login_redirects_to_student_dashboard(self):
        CustomUser.objects.create_user(
            email='oquvchi@roziyev.dev',
            username='oquvchi',
            password='Password123!',
            role=UserRole.STUDENT,
        )
        response = self.client.post(
            reverse('login'),
            {'email': 'oquvchi@roziyev.dev', 'password': 'Password123!'}
        )
        self.assertRedirects(response, reverse('student_dashboard'))

    def test_student_sidebar_persists_across_pages(self):
        CustomUser.objects.create_user(
            email='oquvchi2@roziyev.dev',
            username='oquvchi2',
            password='Password123!',
            role=UserRole.STUDENT,
        )
        self.client.login(email='oquvchi2@roziyev.dev', password='Password123!')

        for url_name in ('student_dashboard', 'profile', 'profile_settings', 'my_certificates', 'course_list', 'home'):
            res = self.client.get(reverse(url_name))
            self.assertEqual(res.status_code, 200)
            self.assertContains(res, 'id="student-sidebar"')
            self.assertContains(res, 'id="sidebar-logo-toggle"')
            self.assertContains(res, 'toggleStudentSidebar()')
