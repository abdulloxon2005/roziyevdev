import json

from django.test import TestCase, override_settings
from django.urls import reverse

from apps.core.code_runner import run_python
from apps.courses.models import Course, Lesson
from apps.interactive.content import python_module1
from apps.interactive.grading import grade_task
from apps.interactive.models import (
    AssessmentAttempt,
    LessonBlock,
    ModuleAssessment,
    Task,
    TaskAttempt,
    TaskKind,
    TaskProgress,
    TaskSection,
)
from apps.interactive.seeding import seed_course
from apps.interactive.validation import check_task
from apps.learning.models import Enrollment, LessonProgress
from apps.learning.services import enroll_user
from apps.users.models import CustomUser

# Testlarda so'rovlar chastotasi cheklovi xalaqit bermasligi uchun
RUNNER = {'BACKEND': 'subprocess', 'RATE_LIMIT_PER_MINUTE': 0, 'TIMEOUT_SECONDS': 4}


@override_settings(CODE_RUNNER=RUNNER)
class SandboxTests(TestCase):
    """Kod bajarish izolyatsiyalangan jarayonda va cheklovlar bilan ishlashi."""

    def test_hello_world(self):
        res = run_python('print("Salom, dunyo!")')
        self.assertEqual(res.status, 'ok')
        self.assertEqual(res.stdout, "Salom, dunyo!\n")

    def test_name_error_is_structured_and_explained(self):
        res = run_python('x = 1\nprint(y)')
        self.assertEqual(res.status, 'error')
        self.assertEqual(res.error['type'], 'NameError')
        self.assertEqual(res.error['line'], 2)
        self.assertIn("2-qatorda", res.friendly_error)

    def test_syntax_error(self):
        res = run_python('print("salom"')
        self.assertEqual(res.status, 'syntax_error')
        self.assertIn('yopilmagan', res.friendly_error)

    def test_infinite_loop_times_out(self):
        res = run_python('while True:\n    pass')
        self.assertEqual(res.status, 'timeout')

    def test_network_and_processes_blocked(self):
        for code in ('import socket', 'import os\nos.system("echo hi")', 'import subprocess'):
            res = run_python(code)
            self.assertNotEqual(res.status, 'ok', code)
            self.assertEqual(res.error['type'], 'PermissionError', code)

    def test_filesystem_blocked(self):
        self.assertNotEqual(run_python('open("x.txt", "w").write("a")').status, 'ok')
        self.assertNotEqual(run_python('print(open("manage.py").read())').status, 'ok')

    def test_secrets_not_leaked_through_environment(self):
        res = run_python('import os\nprint(sorted(os.environ))')
        self.assertEqual(res.status, 'ok')
        self.assertNotIn('DJANGO', res.stdout)
        self.assertNotIn('SECRET', res.stdout)

    def test_output_is_limited(self):
        res = run_python('while True:\n    print("x" * 1000)')
        self.assertIn(res.status, ('output_limit', 'timeout'))
        self.assertLessEqual(len(res.stdout), 20001)

    def test_input_and_multifile(self):
        self.assertEqual(run_python('print("Salom", input())', stdin='Ali\n').stdout, "Salom Ali\n")
        res = run_python(files={'main.py': 'from utils import f\nprint(f(2))', 'utils.py': 'def f(x):\n    return x * 10'})
        self.assertEqual(res.stdout, "20\n")

    @override_settings(CODE_RUNNER={**RUNNER, 'BACKEND': 'disabled'})
    def test_disabled_backend_never_fakes_output(self):
        res = run_python('print(1)')
        self.assertEqual(res.status, 'unavailable')
        self.assertEqual(res.stdout, '')


class SeedMixin:
    @classmethod
    def setUpTestData(cls):
        cls.admin = CustomUser.objects.create_superuser(email='admin@t.uz', username='admin', password='Parol12345!')
        cls.course, _ = seed_course(python_module1)
        cls.module = cls.course.modules.get(order=1)
        cls.lessons = list(Lesson.objects.filter(module=cls.module).order_by('order'))
        cls.student = CustomUser.objects.create_user(email='s@t.uz', username='s', password='Parol12345!')
        cls.outsider = CustomUser.objects.create_user(email='o@t.uz', username='o', password='Parol12345!')
        enroll_user(cls.student, cls.course)

    def task(self, lesson_no, section, kind=None):
        qs = Task.objects.filter(lesson=self.lessons[lesson_no - 1], section=section)
        if kind:
            qs = qs.filter(kind=kind)
        return qs.order_by('order').first()

    def post_json(self, url, data):
        return self.client.post(url, data=json.dumps(data), content_type='application/json')


@override_settings(CODE_RUNNER=RUNNER)
class SeedContentTests(SeedMixin, TestCase):
    """Dastlabki kontent talablarga mos va har bir yechim haqiqatan ishlaydi."""

    def test_structure(self):
        self.assertEqual(self.course.title, "Python — 0 dan boshlash")
        self.assertEqual(self.module.title, "Birinchi qadamlar")
        self.assertEqual(len(self.lessons), 6)
        for lesson in self.lessons:
            tasks = Task.objects.filter(lesson=lesson)
            self.assertTrue(lesson.is_interactive)
            self.assertTrue(lesson.objective and lesson.concept_list, lesson.title)
            self.assertGreaterEqual(LessonBlock.objects.filter(lesson=lesson, block_type='code').count(), 1, lesson.title)
            self.assertGreaterEqual(LessonBlock.objects.filter(lesson=lesson, block_type='task').count(), 1, lesson.title)
            self.assertTrue(2 <= tasks.filter(section=TaskSection.QUIZ).count() <= 3, lesson.title)
            self.assertEqual(tasks.filter(section=TaskSection.ASSIGNMENT).count(), 1, lesson.title)
            self.assertGreaterEqual(tasks.filter(section=TaskSection.REVIEW).count(), 1, lesson.title)
            self.assertEqual(set(tasks.filter(section=TaskSection.PRACTICE).values_list('difficulty', flat=True)), {'easy', 'medium', 'hard'})
            assignment = tasks.get(section=TaskSection.ASSIGNMENT)
            self.assertTrue(assignment.hint and assignment.full_solution and assignment.tests.exists(), lesson.title)
        assessment = ModuleAssessment.objects.get(module=self.module)
        kinds = [i.task.kind for i in assessment.items.select_related('task')]
        self.assertEqual(sum(k in ('single_choice', 'multiple_choice') for k in kinds), 5)
        self.assertEqual(kinds.count('predict_output'), 3)
        self.assertEqual(kinds.count('find_error'), 2)
        self.assertEqual(assessment.items.filter(task__section='project').count(), 1)
        self.assertEqual(assessment.pass_percent, 70)

    def test_logical_name(self):
        task = self.task(3, TaskSection.ASSIGNMENT)
        self.assertEqual(task.logical_name, "Python / 1-modul / 3-dars / Vazifa-1")

    def test_every_task_is_valid_against_sandbox(self):
        for task in Task.objects.filter(module=self.module).prefetch_related('options', 'tests'):
            problems = [m for level, m in check_task(task) if level != 'ok']
            self.assertEqual(problems, [], task.logical_name)

    def test_seed_is_idempotent(self):
        _, created = seed_course(python_module1)
        self.assertFalse(created)
        self.assertEqual(Course.objects.filter(slug=python_module1.COURSE['slug']).count(), 1)


class SeedCategoryTests(TestCase):
    def test_reuses_existing_python_category(self):
        from apps.courses.models import Category
        existing = Category.objects.create(name='Backend & Python Dasturlash', slug='backend-python')
        course, _ = seed_course(python_module1)
        self.assertEqual(course.category, existing)
        self.assertEqual(Category.objects.count(), 1)


@override_settings(CODE_RUNNER=RUNNER)
class GradingTests(SeedMixin, TestCase):
    def test_choice(self):
        task = self.task(1, TaskSection.QUIZ, TaskKind.SINGLE_CHOICE)
        right = task.options.get(is_correct=True)
        wrong = task.options.filter(is_correct=False).first()
        self.assertTrue(grade_task(task, {'options': [right.id]}).is_correct)
        self.assertFalse(grade_task(task, {'options': [wrong.id]}).is_correct)

    def test_predict_output_normalizes_trailing_spaces(self):
        task = self.task(3, TaskSection.QUIZ, TaskKind.PREDICT_OUTPUT)
        self.assertTrue(grade_task(task, {'text': "10  \n5 + 5\n\n"}).is_correct)
        self.assertFalse(grade_task(task, {'text': "10\n10"}).is_correct)

    def test_code_task_requires_tests_not_just_running(self):
        task = self.task(3, TaskSection.ASSIGNMENT)
        runs_but_wrong = grade_task(task, {}, 'print("Salom")')
        self.assertTrue(runs_but_wrong.run.ok)
        self.assertFalse(runs_but_wrong.is_correct)
        good = grade_task(task, {}, task.full_solution)
        self.assertTrue(good.is_correct)
        self.assertEqual(good.score, task.points)

    def test_fill_blank(self):
        task = self.task(3, TaskSection.INLINE, TaskKind.FILL_BLANK)
        self.assertTrue(grade_task(task, {'blanks': ['print']}).is_correct)
        self.assertFalse(grade_task(task, {'blanks': ['Print']}).is_correct)


@override_settings(CODE_RUNNER=RUNNER)
class LessonFlowTests(SeedMixin, TestCase):
    def lesson_url(self, n):
        return reverse('course_learn_lesson', args=[self.course.slug, self.lessons[n - 1].id])

    def test_lesson_page_renders_without_leaking_answers(self):
        self.client.force_login(self.student)
        resp = self.client.get(self.lesson_url(3))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'interactive/lesson.html')
        html = resp.content.decode()
        self.assertIn('Vazifani bajarish', html)
        self.assertIn('Python / 1-modul / 3-dars / Vazifa-1', html)
        assignment = self.task(3, TaskSection.ASSIGNMENT)
        self.assertNotIn("Men Python o&#x27;rganyapman.&quot;)", html)  # to'liq yechim sahifaga chiqmaydi
        self.assertNotIn('is_correct', html)

    def test_anonymous_sees_preview_lesson_but_cannot_run(self):
        resp = self.client.get(self.lesson_url(1))
        self.assertEqual(resp.status_code, 200)
        resp = self.post_json(reverse('interactive_run'), {'code': 'print(1)', 'lesson_id': self.lessons[0].id})
        self.assertEqual(resp.status_code, 302)  # login talab qilinadi

    def test_run_requires_access(self):
        self.client.force_login(self.outsider)
        resp = self.post_json(reverse('interactive_run'), {'code': 'print(1)', 'lesson_id': self.lessons[2].id})
        self.assertEqual(resp.status_code, 403)
        self.client.force_login(self.student)
        resp = self.post_json(reverse('interactive_run'), {'code': 'print("Salom, dunyo!")', 'lesson_id': self.lessons[2].id})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['result']['stdout'], "Salom, dunyo!\n")

    def test_check_records_attempts_and_unlocks_solution(self):
        self.client.force_login(self.student)
        task = self.task(3, TaskSection.ASSIGNMENT)
        check_url = reverse('interactive_task_check', args=[task.id])
        reveal_url = reverse('interactive_task_reveal', args=[task.id])

        self.assertEqual(self.post_json(reveal_url, {'what': 'solution'}).status_code, 403)
        self.assertEqual(self.post_json(reveal_url, {'what': 'partial'}).status_code, 403)
        self.assertEqual(self.post_json(reveal_url, {'what': 'hint'}).status_code, 200)

        r1 = self.post_json(check_url, {'code': 'print("Salom, dunyo!")'}).json()
        self.assertFalse(r1['is_correct'])
        self.assertEqual(r1['attempt_number'], 1)
        self.assertEqual(self.post_json(reveal_url, {'what': 'partial'}).status_code, 200)
        self.assertEqual(self.post_json(reveal_url, {'what': 'solution'}).status_code, 403)

        self.post_json(check_url, {'code': 'print("x")'})
        sol = self.post_json(reveal_url, {'what': 'solution'})
        self.assertEqual(sol.status_code, 200)
        self.assertIn('solution', sol.json())

        r3 = self.post_json(check_url, {'code': task.full_solution}).json()
        self.assertTrue(r3['is_correct'])
        self.assertTrue(r3['solved'])
        progress = TaskProgress.objects.get(user=self.student, task=task)
        self.assertEqual(progress.attempts_count, 3)
        self.assertTrue(progress.solution_viewed)
        self.assertEqual(TaskAttempt.objects.filter(user=self.student, task=task).count(), 3)
        self.assertEqual(r3['coins_awarded'], 0)  # yechim ko'rilgandan keyin tanga berilmaydi

        history = self.client.get(reverse('interactive_task_attempts', args=[task.id])).json()
        self.assertEqual(len(history['attempts']), 3)

    def test_coins_for_independent_solution(self):
        self.client.force_login(self.student)
        task = self.task(1, TaskSection.ASSIGNMENT)
        body = self.post_json(reverse('interactive_task_check', args=[task.id]), {'code': task.full_solution}).json()
        self.assertTrue(body['is_correct'])
        self.assertGreater(body['coins_awarded'], 0)

    def test_outsider_cannot_check_or_see_history(self):
        self.client.force_login(self.outsider)
        task = self.task(3, TaskSection.ASSIGNMENT)
        self.assertEqual(self.post_json(reverse('interactive_task_check', args=[task.id]), {'code': 'print(1)'}).status_code, 404)
        self.assertEqual(self.client.get(reverse('interactive_task_attempts', args=[task.id])).status_code, 404)

    def test_draft_autosave(self):
        self.client.force_login(self.student)
        lesson = self.lessons[2]
        resp = self.post_json(reverse('interactive_draft_save'), {'lesson_id': lesson.id, 'key': 'playground', 'code': 'print(42)'})
        self.assertEqual(resp.status_code, 200)
        page = self.client.get(self.lesson_url(3))
        self.assertIn('print(42)', page.content.decode())

    def test_draft_lessons_hidden_from_students(self):
        lesson = self.lessons[5]
        lesson.is_published = False
        lesson.save()
        self.client.force_login(self.student)
        resp = self.client.get(self.lesson_url(6))
        self.assertNotEqual(resp.context.get('current_lesson'), lesson)
        task = self.task(6, TaskSection.ASSIGNMENT)
        self.assertEqual(self.post_json(reverse('interactive_task_check', args=[task.id]), {'code': 'print(1)'}).status_code, 404)
        self.client.force_login(self.admin)
        resp = self.client.get(self.lesson_url(6))
        self.assertEqual(resp.context['current_lesson'], lesson)
        self.assertContains(resp, "Oldindan ko'rish rejimi")


@override_settings(CODE_RUNNER=RUNNER)
class AssessmentTests(SeedMixin, TestCase):
    def setUp(self):
        self.assessment = ModuleAssessment.objects.get(module=self.module)
        self.url = reverse('interactive_assessment', args=[self.assessment.id])

    def complete_all_lessons(self):
        enrollment = Enrollment.objects.get(user=self.student, course=self.course)
        for lesson in self.lessons:
            LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)

    def answers(self, correct=True):
        data = {}
        for item in self.assessment.ordered_items():
            t = item.task
            key = f"t{t.id}"
            if t.is_choice:
                opts = t.options.filter(is_correct=correct)
                data[f"{key}_opt"] = [str(o.id) for o in opts][:1] if t.kind == 'single_choice' else [str(o.id) for o in opts]
            elif t.kind == 'predict_output':
                data[f"{key}_text"] = t.correct_answer if correct else 'xato'
            else:
                data[f"{key}_code"] = t.full_solution if correct else t.starter_code
        return data

    def test_locked_until_all_lessons_completed(self):
        self.client.force_login(self.student)
        resp = self.client.get(self.url)
        self.assertFalse(resp.context['status']['unlocked'])
        resp = self.client.post(self.url, self.answers())
        self.assertEqual(AssessmentAttempt.objects.count(), 0)

    def test_pass_and_retake(self):
        self.complete_all_lessons()
        self.client.force_login(self.student)
        self.assertTrue(self.client.get(self.url).context['status']['can_attempt'])

        self.client.post(self.url, self.answers(correct=False))
        failed = AssessmentAttempt.objects.get(user=self.student)
        self.assertFalse(failed.passed)

        resp = self.client.post(self.url, self.answers(correct=True))
        best = AssessmentAttempt.objects.filter(user=self.student).order_by('-attempt_number').first()
        self.assertRedirects(resp, reverse('interactive_assessment_result', args=[best.id]))
        self.assertEqual(best.attempt_number, 2)
        self.assertTrue(best.passed)
        self.assertEqual(best.percent, 100)
        self.assertEqual(best.answers.count(), self.assessment.items.count())
        self.assertEqual(self.client.get(resp.url).status_code, 200)

        # Boshqa o'quvchi natijani ko'ra olmaydi
        self.client.force_login(self.outsider)
        self.assertEqual(self.client.get(resp.url).status_code, 404)

    def test_pass_percent_is_configurable(self):
        self.complete_all_lessons()
        self.assessment.pass_percent = 100
        self.assessment.save()
        data = self.answers(correct=True)
        first_choice = next(k for k in data if k.endswith('_opt'))
        data[first_choice] = []  # bitta savolni bo'sh qoldiramiz
        self.client.force_login(self.student)
        self.client.post(self.url, data)
        attempt = AssessmentAttempt.objects.get(user=self.student)
        self.assertLess(attempt.percent, 100)
        self.assertFalse(attempt.passed)

    def test_progress_page(self):
        self.client.force_login(self.student)
        resp = self.client.get(reverse('interactive_course_progress', args=[self.course.slug]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Birinchi qadamlar")
        self.assertEqual(self.client.get(reverse('interactive_my_learning')).status_code, 200)


@override_settings(CODE_RUNNER=RUNNER)
class DashboardContentTests(SeedMixin, TestCase):
    def test_students_cannot_manage_content(self):
        self.client.force_login(self.student)
        lesson = self.lessons[0]
        resp = self.client.get(reverse('dashboard_lesson_interactive', args=[self.course.slug, lesson.id]))
        self.assertEqual(resp.status_code, 302)
        resp = self.client.post(reverse('dashboard_lesson_interactive', args=[self.course.slug, lesson.id]),
                                {'block_type': 'text', 'order': 99, 'body': 'hack'})
        self.assertFalse(LessonBlock.objects.filter(body='hack').exists())

    def test_admin_pages_render(self):
        self.client.force_login(self.admin)
        lesson = self.lessons[2]
        task = self.task(3, TaskSection.ASSIGNMENT)
        for url in (
            reverse('dashboard_course_curriculum', args=[self.course.slug]),
            reverse('dashboard_lesson_interactive', args=[self.course.slug, lesson.id]),
            reverse('dashboard_task_edit', args=[self.course.slug, task.id]),
            reverse('dashboard_task_create', args=[self.course.slug, self.module.id]) + f'?lesson={lesson.id}&section=quiz',
            reverse('dashboard_module_assessment', args=[self.course.slug, self.module.id]),
            reverse('dashboard_lesson_edit', args=[self.course.slug, lesson.id]),
        ):
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_admin_adds_block_and_task_without_code_changes(self):
        self.client.force_login(self.admin)
        lesson = self.lessons[0]
        url = reverse('dashboard_lesson_interactive', args=[self.course.slug, lesson.id])
        self.client.post(url, {'block_type': 'code', 'order': 50, 'title': 'Yangi misol', 'code': 'print(7)', 'is_runnable': 'on', 'callout_style': 'info'})
        self.assertTrue(LessonBlock.objects.filter(lesson=lesson, title='Yangi misol').exists())

        create = reverse('dashboard_task_create', args=[self.course.slug, self.module.id])
        data = {
            'lesson': lesson.id, 'section': 'practice', 'kind': 'code', 'difficulty': 'easy', 'order': 9, 'points': 3,
            'is_published': 'on', 'title': 'Yetti', 'prompt': '7 ni chiqaring', 'full_solution': 'print(7)',
            'solution_unlock_attempts': 2,
            'opt-TOTAL_FORMS': 0, 'opt-INITIAL_FORMS': 0, 'opt-MIN_NUM_FORMS': 0, 'opt-MAX_NUM_FORMS': 1000,
            'test-TOTAL_FORMS': 1, 'test-INITIAL_FORMS': 0, 'test-MIN_NUM_FORMS': 0, 'test-MAX_NUM_FORMS': 1000,
            'test-0-order': 1, 'test-0-description': '7 chiqadi', 'test-0-check_type': 'output_equals', 'test-0-expected': '7',
        }
        self.client.post(create, data)
        task = Task.objects.get(title='Yetti')
        self.assertEqual(task.module, self.module)
        self.assertEqual(task.tests.count(), 1)
        self.assertEqual([lvl for lvl, _ in check_task(task)], ['ok'])

    def test_reorder_lessons(self):
        self.client.force_login(self.admin)
        first, second = self.lessons[0], self.lessons[1]
        self.client.post(reverse('dashboard_lesson_move', args=[self.course.slug, second.id, 'up']))
        first.refresh_from_db()
        second.refresh_from_db()
        self.assertLess(second.order, first.order)


@override_settings(CODE_RUNNER=RUNNER)
class ProjectsIntegrationTests(TestCase):
    def test_project_ide_runs_in_sandbox_with_multiple_files(self):
        from apps.projects.models import Project, ProjectFile
        user = CustomUser.objects.create_user(email='p@t.uz', username='p', password='Parol12345!')
        project = Project.objects.create(author=user, title='Loyiha', language='python')
        main = project.create_default_files()
        self.client.force_login(user)
        resp = self.client.post(reverse('student_project_run', args=[project.id]), {'file_id': main.id, 'code': main.content})
        body = resp.json()
        self.assertTrue(body['success'], body)
        self.assertIn('Assalomu alaykum', body['output'])
        ProjectFile.objects.create(project=project, name='bad.py', content='import socket')
        bad = project.files.get(name='bad.py')
        body = self.client.post(reverse('student_project_run', args=[project.id]), {'file_id': bad.id}).json()
        self.assertFalse(body['success'])

    def test_run_with_readme_selected_runs_entry_point(self):
        from apps.projects.models import Project
        user = CustomUser.objects.create_user(email='r@t.uz', username='r', password='Parol12345!')
        project = Project.objects.create(author=user, title='Readme', language='python')
        project.create_default_files()
        readme = project.files.get(name='README.md')
        self.client.force_login(user)
        body = self.client.post(reverse('student_project_run', args=[project.id]), {'file_id': readme.id, 'code': readme.content}).json()
        self.assertTrue(body['success'], body)
        self.assertIn('Assalomu alaykum', body['output'])

    def test_unsupported_language_is_honest(self):
        from apps.projects.models import Project
        user = CustomUser.objects.create_user(email='q@t.uz', username='q', password='Parol12345!')
        project = Project.objects.create(author=user, title='Java', language='java')
        main = project.create_default_files()
        self.client.force_login(user)
        body = self.client.post(reverse('student_project_run', args=[project.id]), {'file_id': main.id}).json()
        self.assertFalse(body['success'])
        self.assertIn("qo'llab-quvvatlanmaydi", body['output'])
