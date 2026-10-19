from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser, UserRole
from apps.courses.models import Category, Course, CourseLevel, CourseModule, Lesson, LessonType
from apps.learning.models import Assignment, Enrollment, AssignmentSubmission, SubmissionStatus
from apps.orders.models import Order, OrderStatus


class DashboardAccessTests(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='student',
            email='student@example.com',
            password='testpassword123',
            role=UserRole.STUDENT,
        )
        self.instructor = CustomUser.objects.create_user(
            username='instructor',
            email='instructor@example.com',
            password='testpassword123',
            role=UserRole.INSTRUCTOR,
            is_staff=True,
        )

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(reverse('dashboard_index'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_student_forbidden_and_redirected_to_home(self):
        self.client.login(email='student@example.com', password='testpassword123')
        response = self.client.get(reverse('dashboard_index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_instructor_allowed(self):
        self.client.login(email='instructor@example.com', password='testpassword123')
        response = self.client.get(reverse('dashboard_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ustoz Studiyasi")


class CourseCrudDashboardTests(TestCase):
    def setUp(self):
        self.instructor = CustomUser.objects.create_user(
            username='instructor2',
            email='instructor2@example.com',
            password='testpassword123',
            role=UserRole.INSTRUCTOR,
            is_staff=True,
        )
        self.category = Category.objects.create(name='Algoritmlar', icon='fa-solid fa-code')
        self.client.login(email='instructor2@example.com', password='testpassword123')

    def test_create_course(self):
        response = self.client.post(reverse('dashboard_course_create'), {
            'title': 'Dart va Flutter Asoslari',
            'category': self.category.id,
            'level': CourseLevel.BEGINNER,
            'price': 150000,
            'is_free': False,
            'duration_hours': 10,
            'short_description': "Flutter kursi qisqa tavsifi",
            'description': "Flutter kursi to'liq tavsifi",
            'what_you_will_learn': "Dart\nFlutter UI",
            'requirements': "Kompyuter",
            'is_published': True,
        })
        course = Course.objects.filter(title='Dart va Flutter Asoslari').first()
        self.assertIsNotNone(course)
        self.assertRedirects(response, reverse('dashboard_course_curriculum', kwargs={'slug': course.slug}))
        self.assertEqual(course.instructor, self.instructor)
        self.assertEqual(course.price, Decimal('150000'))

    def test_edit_course(self):
        course = Course.objects.create(
            title='Eski Kurs',
            instructor=self.instructor,
            category=self.category,
            short_description='Qisqa',
            description='To\'liq',
            price=50000,
        )
        response = self.client.post(reverse('dashboard_course_edit', kwargs={'slug': course.slug}), {
            'title': 'Yangilangan Kurs Nomi',
            'category': self.category.id,
            'level': CourseLevel.ADVANCED,
            'price': 99000,
            'is_free': False,
            'duration_hours': 15,
            'short_description': 'Yangi qisqa',
            'description': 'Yangi to\'liq',
            'is_published': True,
        })
        course.refresh_from_db()
        self.assertEqual(course.title, 'Yangilangan Kurs Nomi')
        self.assertEqual(course.price, Decimal('99000'))

    def test_delete_course(self):
        course = Course.objects.create(
            title='O\'chiriladigan Kurs',
            instructor=self.instructor,
            category=self.category,
            short_description='Qisqa',
            description='To\'liq',
        )
        response = self.client.post(reverse('dashboard_course_delete', kwargs={'slug': course.slug}))
        self.assertRedirects(response, reverse('dashboard_courses_list'))
        self.assertFalse(Course.objects.filter(id=course.id).exists())


class CurriculumAndLessonDashboardTests(TestCase):
    def setUp(self):
        self.instructor = CustomUser.objects.create_user(
            username='instructor3',
            email='instructor3@example.com',
            password='testpassword123',
            role=UserRole.INSTRUCTOR,
            is_staff=True,
        )
        self.category = Category.objects.create(name='Mobil', icon='fa-solid fa-mobile')
        self.course = Course.objects.create(
            title='Mobil Dasturlash',
            instructor=self.instructor,
            category=self.category,
            short_description='Qisqa',
            description='To\'liq',
        )
        self.client.login(email='instructor3@example.com', password='testpassword123')

    def test_add_module(self):
        response = self.client.post(reverse('dashboard_module_create', kwargs={'slug': self.course.slug}), {
            'title': '1-Modul: Kirish',
            'order': 1,
        })
        self.assertRedirects(response, reverse('dashboard_course_curriculum', kwargs={'slug': self.course.slug}))
        module = CourseModule.objects.filter(course=self.course, title='1-Modul: Kirish').first()
        self.assertIsNotNone(module)

    def test_add_lesson_with_assignment(self):
        module = CourseModule.objects.create(course=self.course, title='Asosiy Modul', order=1)
        response = self.client.post(reverse('dashboard_lesson_create', kwargs={'slug': self.course.slug, 'module_id': module.id}), {
            'module': module.id,
            'title': '1.1 O\'zgaruvchilar va tiplar',
            'lesson_type': LessonType.VIDEO,
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'content': 'Dars konspekti matni...',
            'duration_minutes': 20,
            'order': 1,
            'is_preview': True,
            # Integrated Assignment fields
            'has_assignment': True,
            'assignment_title': 'O\'zgaruvchilar bo\'yicha amaliy mashq',
            'assignment_description': 'Qiymatni ekranga chiqaring',
            'starter_code': 'void main() {}',
            'coin_reward': 60,
            'max_score': 100,
            'passing_score': 75,
            'allow_code': True,
            'allow_flowchart': True,
            'allow_file_upload': True,
            'assignment_is_active': True,
        })
        self.assertRedirects(response, reverse('dashboard_course_curriculum', kwargs={'slug': self.course.slug}))
        lesson = Lesson.objects.filter(module=module, title='1.1 O\'zgaruvchilar va tiplar').first()
        self.assertIsNotNone(lesson)
        self.assertEqual(lesson.duration_minutes, 20)
        self.assertTrue(lesson.is_preview)
        self.assertTrue(lesson.has_video)

        # Check attached Assignment
        assignment = getattr(lesson, 'assignment', None)
        self.assertIsNotNone(assignment)
        self.assertEqual(assignment.coin_reward, 60)
        self.assertEqual(assignment.passing_score, 75)
        self.assertTrue(assignment.allow_code)
        self.assertTrue(assignment.allow_flowchart)

    def test_students_and_orders_views(self):
        # Create student enrollment and order
        student = CustomUser.objects.create_user(username='std1', email='std1@test.com', password='p1', coins=50)
        Enrollment.objects.create(user=student, course=self.course, progress_percent=45)
        Order.objects.create(user=student, course=self.course, amount=120000, status=OrderStatus.PAID)

        # Check students view
        resp_students = self.client.get(reverse('dashboard_students_list'))
        self.assertEqual(resp_students.status_code, 200)
        self.assertContains(resp_students, 'std1@test.com')
        self.assertContains(resp_students, '45%')

        # Check orders view
        resp_orders = self.client.get(reverse('dashboard_orders_list'))
        self.assertEqual(resp_orders.status_code, 200)
        self.assertContains(resp_orders, 'std1@test.com')
        self.assertContains(resp_orders, "so'm")
        self.assertContains(resp_orders, 'ORD-')

        # Check reviews view
        resp_reviews = self.client.get(reverse('dashboard_reviews_list'))
        self.assertEqual(resp_reviews.status_code, 200)


class ApiDocsHiddenTests(TestCase):
    """API hujjatlari faqat adminlarga ochiq, boshqalarga 404."""

    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username='docstudent', email='docstudent@example.com', password='testpassword123',
        )
        self.admin = CustomUser.objects.create_user(
            username='docadmin', email='docadmin@example.com', password='testpassword123', is_staff=True,
        )

    def test_anonymous_gets_404(self):
        for name in ('swagger-ui', 'redoc', 'schema'):
            self.assertEqual(self.client.get(reverse(name)).status_code, 404)

    def test_student_gets_404(self):
        self.client.login(email='docstudent@example.com', password='testpassword123')
        for name in ('swagger-ui', 'redoc', 'schema'):
            self.assertEqual(self.client.get(reverse(name)).status_code, 404)

    def test_staff_can_open_docs(self):
        self.client.login(email='docadmin@example.com', password='testpassword123')
        self.assertEqual(self.client.get(reverse('swagger-ui')).status_code, 200)

    def test_home_has_no_api_link(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, '/api/docs/')
