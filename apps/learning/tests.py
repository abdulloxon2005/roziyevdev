from django.test import TestCase
from django.urls import reverse
from apps.users.models import CustomUser
from apps.courses.models import Course, Category, CourseModule, Lesson
from apps.learning.models import (
    Enrollment,
    LessonProgress,
    Assignment,
    AssignmentSubmission,
    SubmissionStatus,
    CoinTransaction,
)
from apps.learning.services import enroll_user, mark_lesson_complete


class LearningTestCase(TestCase):
    def setUp(self):
        self.instructor = CustomUser.objects.create_user(
            username="instructor_test",
            email="instructor@example.com",
            password="password123",
            is_staff=True
        )
        self.user = CustomUser.objects.create_user(
            username="student_test",
            email="student_test@example.com",
            password="password123"
        )
        self.category = Category.objects.create(name="Mobile", slug="mobile")
        self.course = Course.objects.create(
            title="Flutter Basics",
            slug="flutter-basics",
            category=self.category,
            is_free=True
        )
        self.module = CourseModule.objects.create(course=self.course, title="Module 1", order=1)
        self.lesson1 = Lesson.objects.create(module=self.module, title="Lesson 1", order=1)
        self.lesson2 = Lesson.objects.create(module=self.module, title="Lesson 2", order=2)

    def test_enrollment_and_progress(self):
        enrollment, created = enroll_user(self.user, self.course)
        self.assertTrue(created)
        self.assertEqual(enrollment.progress_percent, 0)
        self.assertFalse(enrollment.is_completed)

        # 1-darsni tugatish
        just_completed = mark_lesson_complete(enrollment, self.lesson1)
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.progress_percent, 50)
        self.assertFalse(just_completed)

        # 2-darsni tugatish (100%)
        just_completed = mark_lesson_complete(enrollment, self.lesson2)
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.progress_percent, 100)
        self.assertTrue(just_completed)
        self.assertTrue(enrollment.is_completed)

    def test_web_player_access(self):
        self.client.login(email="student_test@example.com", password="password123")
        enroll_user(self.user, self.course)

        response = self.client.get(reverse('course_learn', args=[self.course.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Flutter Basics")

    def test_assignment_submission_and_admin_approval_coins(self):
        # 1. Darsga vazifa yaratish
        assignment = Assignment.objects.create(
            lesson=self.lesson1,
            title="Ikki son yig'indisi",
            description="Ikki son yig'indisini hisoblovchi funksiya yozing.",
            starter_code="def add(a, b):\n    pass",
            coin_reward=50,
            passing_score=70
        )
        self.assertEqual(self.user.coins, 0)

        # 2. Talaba topshiriq yuboradi
        submission = AssignmentSubmission.objects.create(
            assignment=assignment,
            student=self.user,
            submitted_code="def add(a, b):\n    return a + b",
            flowchart_data="flowchart TD; Start --> Input --> Calc --> Output --> End"
        )
        self.assertEqual(submission.status, SubmissionStatus.PENDING)
        self.assertEqual(submission.coins_awarded, 0)

        # 3. Admin topshiriqni qabul qiladi va 95 ball qo'yadi
        submission.approve(
            reviewer=self.instructor,
            score=95,
            feedback="A'lo darajada yechilgan! Algoritm ixcham va to'g'ri."
        )

        submission.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(submission.status, SubmissionStatus.APPROVED)
        self.assertEqual(submission.score, 95)
        self.assertEqual(submission.coins_awarded, 50)
        self.assertEqual(self.user.coins, 50)

        # Tangalar tranzaksiyasi yaratilganini tekshirish
        tx = CoinTransaction.objects.filter(student=self.user, submission=submission).first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.amount, 50)

    def test_assignment_rejection(self):
        assignment = Assignment.objects.create(
            lesson=self.lesson2,
            title="Massivni saralash",
            description="Massivni saralang",
            coin_reward=60,
            passing_score=70
        )
        submission = AssignmentSubmission.objects.create(
            assignment=assignment,
            student=self.user,
            submitted_code="wrong code"
        )

        submission.reject(
            reviewer=self.instructor,
            feedback="Kodingizda xatolik bor, shartni qayta o'qing.",
            score=40
        )

        submission.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(submission.status, SubmissionStatus.REJECTED)
        self.assertEqual(submission.score, 40)
        self.assertEqual(submission.coins_awarded, 0)
        self.assertEqual(self.user.coins, 0)

    def test_web_submit_assignment_endpoint(self):
        enroll_user(self.user, self.course)
        assignment = Assignment.objects.create(
            lesson=self.lesson1,
            title="Form orqali vazifa",
            description="Tavsif",
            coin_reward=40,
            passing_score=60
        )
        self.client.login(email="student_test@example.com", password="password123")
        post_data = {
            'submitted_code': 'print("salom dunyo")',
            'flowchart_data': 'graph TD; S([Start]) --> E([End])'
        }
        res = self.client.post(reverse('submit_assignment', args=[assignment.id]), data=post_data)
        self.assertEqual(res.status_code, 302)

        sub = AssignmentSubmission.objects.filter(assignment=assignment, student=self.user).first()
        self.assertIsNotNone(sub)
        self.assertEqual(sub.status, SubmissionStatus.PENDING)
        self.assertIn("salom dunyo", sub.submitted_code)
        self.assertIn("Start", sub.flowchart_data)

    def test_instructor_review_desk_views(self):
        enroll_user(self.user, self.course)
        assignment = Assignment.objects.create(
            lesson=self.lesson1,
            title="Tekshirish vazifasi",
            description="Tavsif",
            coin_reward=70,
            passing_score=60
        )
        submission = AssignmentSubmission.objects.create(
            assignment=assignment,
            student=self.user,
            submitted_code="result = 100",
            flowchart_data="graph TD; A --> B"
        )

        # 1. Oddiy talaba tekshirish paneliga kira olmasligi kerak
        self.client.login(email="student_test@example.com", password="password123")
        res = self.client.get(reverse('submissions_review_list'))
        self.assertEqual(res.status_code, 302)

        # 2. O'qituvchi/Admin panelga kira oladi
        self.client.login(email="instructor@example.com", password="password123")
        res = self.client.get(reverse('submissions_review_list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "Tekshirish & Baholash")
        self.assertContains(res, self.user.display_name)

        # 3. O'qituvchi batafsil ko'rish sahifasiga kiradi
        detail_res = self.client.get(reverse('submission_review_detail', args=[submission.id]))
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, "result = 100")

        # 4. O'qituvchi baholaydi va qabul qiladi
        post_review = {
            'action': 'approve',
            'score': 88,
            'feedback': 'Yaxshi bajarilgan'
        }
        post_res = self.client.post(reverse('submission_review_detail', args=[submission.id]), data=post_review)
        self.assertEqual(post_res.status_code, 302)

        submission.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(submission.status, SubmissionStatus.APPROVED)
        self.assertEqual(submission.score, 88)
        self.assertEqual(submission.coins_awarded, 70)
        self.assertEqual(self.user.coins, 70)

    def test_auto_mark_lesson_complete_on_approve(self):
        enrollment, _ = enroll_user(self.user, self.course)
        assignment = Assignment.objects.create(
            lesson=self.lesson1,
            title="Auto complete task",
            description="Tavsif",
            coin_reward=30,
            passing_score=70
        )
        submission = AssignmentSubmission.objects.create(
            assignment=assignment,
            student=self.user,
            submitted_code="pass"
        )
        # Boshida dars tugatilmagan
        self.assertFalse(LessonProgress.objects.filter(enrollment=enrollment, lesson=self.lesson1).exists())

        # Qabul qilinganda avtomatik tugallanishi kerak
        submission.approve(reviewer=self.instructor, score=85, feedback="Zo'r")
        self.assertTrue(LessonProgress.objects.filter(enrollment=enrollment, lesson=self.lesson1).exists())

    def test_reject_revokes_coins_if_previously_approved(self):
        assignment = Assignment.objects.create(
            lesson=self.lesson1,
            title="Revoke test",
            description="Tavsif",
            coin_reward=50,
            passing_score=70
        )
        submission = AssignmentSubmission.objects.create(
            assignment=assignment,
            student=self.user,
            submitted_code="pass"
        )
        submission.approve(reviewer=self.instructor, score=90, feedback="Tasdiq")
        self.user.refresh_from_db()
        self.assertEqual(self.user.coins, 50)

        # Endi ustoz uni qaytarib rad etadi
        submission.reject(reviewer=self.instructor, feedback="Bekor qilindi", score=30)
        self.user.refresh_from_db()
        submission.refresh_from_db()
        self.assertEqual(self.user.coins, 0)
        self.assertEqual(submission.coins_awarded, 0)

        # Eng oxirgi tranzaksiya jurnali tekshiriladi (ordering = ['-created_at'])
        tx = CoinTransaction.objects.filter(student=self.user, submission=submission).first()
        self.assertEqual(tx.amount, -50)

    def test_cannot_resubmit_approved_assignment(self):
        enroll_user(self.user, self.course)
        assignment = Assignment.objects.create(
            lesson=self.lesson1,
            title="Lock test",
            description="Tavsif",
            coin_reward=40,
            passing_score=60
        )
        submission = AssignmentSubmission.objects.create(
            assignment=assignment,
            student=self.user,
            submitted_code="good code"
        )
        submission.approve(reviewer=self.instructor, score=90)

        self.client.login(email="student_test@example.com", password="password123")
        res = self.client.post(
            reverse('submit_assignment', args=[assignment.id]),
            data={'submitted_code': 'new code'}
        )
        self.assertEqual(res.status_code, 302)

        # Status o'zgarmasligi kerak
        submission.refresh_from_db()
        self.assertEqual(submission.status, SubmissionStatus.APPROVED)
        self.assertEqual(submission.submitted_code, "good code")

    def test_file_upload_validation(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        enroll_user(self.user, self.course)
        assignment = Assignment.objects.create(
            lesson=self.lesson1,
            title="File test",
            description="Tavsif",
            coin_reward=20,
            passing_score=60
        )
        self.client.login(email="student_test@example.com", password="password123")

        # Noto'g'ri kengaytma (.exe)
        bad_file = SimpleUploadedFile("malicious.exe", b"binary content", content_type="application/octet-stream")
        res = self.client.post(
            reverse('submit_assignment', args=[assignment.id]),
            data={'attached_file': bad_file}
        )
        self.assertEqual(res.status_code, 302)
        # Bazada yaratilmasligi kerak
        self.assertFalse(AssignmentSubmission.objects.filter(assignment=assignment, student=self.user).exists())

        # To'g'ri kengaytma (.dart)
        good_file = SimpleUploadedFile("main.dart", b"void main() {}", content_type="text/plain")
        res2 = self.client.post(
            reverse('submit_assignment', args=[assignment.id]),
            data={'attached_file': good_file}
        )
        self.assertEqual(res2.status_code, 302)
        self.assertTrue(AssignmentSubmission.objects.filter(assignment=assignment, student=self.user).exists())

