from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
import datetime

from apps.users.models import CustomUser
from apps.courses.models import Course, CourseModule, Lesson, Category
from apps.learning.models import Enrollment, Assignment, AssignmentSubmission, SubmissionStatus
from apps.contests.models import Contest, ContestProblem, ContestCategory
from apps.projects.models import Project, ProjectStatus, ProjectType
from apps.roadmaps.models import RoadmapTrack, RoadmapStage, RoadmapNode


class StudentPortalTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='talaba@roziyev.dev',
            username='talaba',
            password='Password123!',
            first_name='Talaba',
            last_name='Sinov',
            coins=100
        )
        self.category = Category.objects.create(name='Mobil Dasturlash', slug='mobil-dasturlash')
        self.course = Course.objects.create(
            title='Flutter Boshlang\'ich',
            slug='flutter-boshlangich',
            category=self.category,
            price=0,
            is_free=True,
            is_published=True
        )
        self.module = CourseModule.objects.create(course=self.course, title='1-Modul', order=1)
        self.lesson = Lesson.objects.create(module=self.module, title='Dart Asoslari', order=1)
        self.assignment = Assignment.objects.create(
            lesson=self.lesson,
            title='Dart Funksiyalar Vazifasi',
            description='Ikkita sonni qo\'shuvchi funksiya yozing.',
            starter_code='void main() {}',
            coin_reward=50,
            max_score=100,
            passing_score=70
        )
        self.enrollment = Enrollment.objects.create(user=self.user, course=self.course, progress_percent=40)

        # Musobaqa
        now = timezone.now()
        self.contest = Contest.objects.create(
            title='Algoritmik Test Musobaqa',
            slug='algoritmik-test-musobaqa',
            category=ContestCategory.ALGORITHMIC,
            description='Test musobaqa',
            start_time=now - datetime.timedelta(hours=1),
            end_time=now + datetime.timedelta(hours=5),
            is_published=True
        )
        self.problem = ContestProblem.objects.create(
            contest=self.contest,
            order=1,
            title='A Masala',
            description='Masala sharti',
            points=100
        )

        # Dasturchi yo'li
        self.track = RoadmapTrack.objects.create(
            title='Flutter Dasturchi',
            slug='flutter-dasturchi',
            is_active=True
        )
        self.stage = RoadmapStage.objects.create(track=self.track, title='1-Bosqich', order=1)
        self.node = RoadmapNode.objects.create(
            stage=self.stage,
            title='Dart Asoslari',
            summary='Dart tilini o\'rganish',
            linked_lesson=self.lesson,
            order=1
        )

    def test_unauthenticated_access_redirects_to_login(self):
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_student_dashboard_overview_loads(self):
        self.client.login(username='talaba@roziyev.dev', password='Password123!')
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Talaba')
        self.assertContains(response, 'Vazifalar Studiyasi')
        self.assertContains(response, 'Kurs Reytingi')

    def test_student_assignments_hub_loads(self):
        self.client.login(username='talaba@roziyev.dev', password='Password123!')
        response = self.client.get(reverse('student_assignments_hub'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dart Funksiyalar Vazifasi')

    def test_student_assignment_solve_and_submission(self):
        self.client.login(username='talaba@roziyev.dev', password='Password123!')
        # GET solver view
        response = self.client.get(reverse('student_assignment_solve', kwargs={'assignment_id': self.assignment.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Kod Muharriri')

        # POST submission
        post_response = self.client.post(
            reverse('student_assignment_solve', kwargs={'assignment_id': self.assignment.id}),
            {'submitted_code': 'int add(int a, int b) { return a + b; }'}
        )
        self.assertEqual(post_response.status_code, 302)
        sub = AssignmentSubmission.objects.filter(assignment=self.assignment, student=self.user).first()
        self.assertIsNotNone(sub)
        self.assertEqual(sub.status, SubmissionStatus.PENDING)
        self.assertIn('int add', sub.submitted_code)

    def test_student_leaderboard_view(self):
        self.client.login(username='talaba@roziyev.dev', password='Password123!')
        response = self.client.get(reverse('student_leaderboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Flutter')
        self.assertContains(response, 'Jonli Guruh Reytingi')

    def test_student_contests_view_and_submission(self):
        self.client.login(username='talaba@roziyev.dev', password='Password123!')
        # List view
        response = self.client.get(reverse('student_contests'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Algoritmik Test Musobaqa')

        # Detail view
        detail_response = self.client.get(reverse('student_contest_detail', kwargs={'slug': self.contest.slug}))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, 'A Masala')

        # Submit solution to problem
        submit_response = self.client.post(
            reverse('student_contest_submit', kwargs={'contest_slug': self.contest.slug, 'problem_id': self.problem.id}),
            {'submitted_code': 'def solution(): return 42'}
        )
        self.assertEqual(submit_response.status_code, 302)

    def test_student_projects_view_create_and_like(self):
        self.client.login(username='talaba@roziyev.dev', password='Password123!')
        # List view
        response = self.client.get(reverse('student_projects'))
        self.assertEqual(response.status_code, 200)

        # Create multi-file project
        create_response = self.client.post(reverse('student_project_create'), {
            'title': 'Test Python Loyiha',
            'language': 'python',
            'project_mode': 'multi_file',
        })
        self.assertEqual(create_response.status_code, 302)
        proj = Project.objects.filter(author=self.user, title='Test Python Loyiha').first()
        self.assertIsNotNone(proj)
        self.assertEqual(proj.language, 'python')
        self.assertEqual(proj.project_mode, 'multi_file')
        # Check default files created
        self.assertTrue(proj.files.filter(name='main.py').exists())
        self.assertTrue(proj.files.filter(name='utils.py').exists())

        # IDE view loads
        ide_response = self.client.get(reverse('student_project_ide', kwargs={'project_id': proj.id}))
        self.assertEqual(ide_response.status_code, 200)
        self.assertContains(ide_response, 'Test Python Loyiha')
        self.assertContains(ide_response, 'Fayllar')

        # File get AJAX
        main_file = proj.files.filter(name='main.py').first()
        get_file_resp = self.client.get(reverse('student_project_file_get', kwargs={'project_id': proj.id, 'file_id': main_file.id}))
        self.assertEqual(get_file_resp.status_code, 200)
        self.assertEqual(get_file_resp.json()['name'], 'main.py')

        # File save AJAX
        save_file_resp = self.client.post(
            reverse('student_project_file_save', kwargs={'project_id': proj.id, 'file_id': main_file.id}),
            {'content': 'print("Yangi kod")'}
        )
        self.assertEqual(save_file_resp.status_code, 200)
        main_file.refresh_from_db()
        self.assertEqual(main_file.content, 'print("Yangi kod")')

        # File create AJAX
        create_file_resp = self.client.post(
            reverse('student_project_file_create', kwargs={'project_id': proj.id}),
            {'name': 'services.py', 'is_folder': 'false'}
        )
        self.assertEqual(create_file_resp.status_code, 200)
        self.assertTrue(proj.files.filter(name='services.py').exists())

        # Run code AJAX
        run_resp = self.client.post(
            reverse('student_project_run', kwargs={'project_id': proj.id}),
            {'code': 'print("Salom dunyo!")', 'file_id': main_file.id}
        )
        self.assertEqual(run_resp.status_code, 200)
        self.assertIn("Salom dunyo!", run_resp.json()['output'])

        # Download ZIP
        zip_resp = self.client.get(reverse('student_project_download_zip', kwargs={'project_id': proj.id}))
        self.assertEqual(zip_resp.status_code, 200)
        self.assertEqual(zip_resp['Content-Type'], 'application/zip')

        # Submit project to instructor
        submit_resp = self.client.post(reverse('student_project_submit', kwargs={'project_id': proj.id}))
        self.assertEqual(submit_resp.status_code, 302)
        proj.refresh_from_db()
        self.assertTrue(proj.is_submitted)
        self.assertEqual(proj.status, ProjectStatus.UNDER_REVIEW)

        # AJAX Like toggle
        like_response = self.client.post(reverse('student_project_like', kwargs={'project_id': proj.id}))
        self.assertEqual(like_response.status_code, 200)
        self.assertTrue(like_response.json()['is_liked'])
        self.assertEqual(like_response.json()['likes_count'], 1)

    def test_student_roadmap_view(self):
        self.client.login(username='talaba@roziyev.dev', password='Password123!')
        response = self.client.get(reverse('student_roadmap_track', kwargs={'track_slug': self.track.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Flutter Dasturchi')
        self.assertContains(response, 'Dart Asoslari')
