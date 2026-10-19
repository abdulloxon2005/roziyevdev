import time
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from apps.users.models import CustomUser


class SessionIdleTimeoutTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='teststudent',
            email='teststudent@example.com',
            password='Password123!',
            first_name='Ali',
            last_name='Valiyev'
        )
        self.client = Client()

    def test_active_user_stays_logged_in(self):
        self.client.login(username='teststudent@example.com', password='Password123!')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

        # Foydalanuvchi tizimda ekanligini tekshiramiz
        session = self.client.session
        self.assertIn('last_activity', session)

    @override_settings(SESSION_IDLE_TIMEOUT=60)
    def test_inactive_user_gets_logged_out(self):
        self.client.login(username='teststudent@example.com', password='Password123!')
        
        # O'tmishdagi vaqtni o'rnatamiz (masalan 120 soniya oldin)
        session = self.client.session
        session['last_activity'] = time.time() - 120
        session.save()

        # Endi yangi so'rov yuborganda middleware logout qilishi kerak
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth/login/', response.url)
        self.assertIn('next=/profile/', response.url)

    @override_settings(SESSION_IDLE_TIMEOUT=60)
    def test_inactive_ajax_request_returns_401(self):
        self.client.login(username='teststudent@example.com', password='Password123!')
        
        session = self.client.session
        session['last_activity'] = time.time() - 120
        session.save()

        response = self.client.get(
            reverse('profile'),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertTrue(data.get('session_expired'))
        self.assertIn('/auth/login/', data.get('redirect'))

    def test_quick_unlock_success(self):
        self.client.login(username='teststudent@example.com', password='Password123!')
        response = self.client.post(
            reverse('quick_unlock'),
            {'password': 'Password123!'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('success'))

    def test_quick_unlock_wrong_password(self):
        self.client.login(username='teststudent@example.com', password='Password123!')
        response = self.client.post(
            reverse('quick_unlock'),
            {'password': 'WrongPassword999'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertFalse(data.get('success'))
        self.assertIn("noto'g'ri", data.get('error'))

    def test_quick_unlock_unauthenticated(self):
        # Chiqib ketgan foydalanuvchi unlock qilmoqchi bo'lsa
        response = self.client.post(
            reverse('quick_unlock'),
            {'password': 'Password123!'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertTrue(data.get('expired'))
