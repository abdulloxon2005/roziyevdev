"""
«Python dasturlash asoslari» kursining 2–11-modullari (7–74-darslar) uchun testlar.

Tekshiriladi: kontent tuzilishi va soni, seed'ning takroran ishga tushirilganda dublikat
yaratmasligi, mavjud ma'lumotlarning saqlanishi, harness (funksiyani turli argumentlar bilan
chaqiruvchi) avtomatik tekshiruvi, o'quvchi jarayoni (dars sahifasi, kodni ishga tushirish,
tekshirish, progress, qoralama, nazorat, takrorlash) va admin sahifalari.

Barcha topshiriqlarni HAQIQIY sandbox'da tekshiruvchi sekin test:
    RUN_SLOW_COURSE_TESTS=1 manage.py test apps.interactive.test_python_course
(shuningdek `manage.py validate_python_content python_m02 ... python_m11` buyrug'i bilan).
"""
import os
import unittest

from django.test import TestCase, override_settings
from django.urls import reverse

from apps.courses.models import Course, CourseModule, Lesson
from apps.interactive.content import python_module1
from apps.interactive.content.registry import COURSE_FULL, MODULE_FILES, load_modules
from apps.interactive.grading import build_harness_code, grade_task
from apps.interactive.models import (
    AssessmentAttempt,
    AssessmentKind,
    CodeDraft,
    LessonBlock,
    ModuleAssessment,
    Task,
    TaskAttempt,
    TaskProgress,
    TaskSection,
    TaskTest,
)
from apps.interactive.seeding import seed_course, seed_module
from apps.interactive.services import course_progress_summary
from apps.interactive.tests import RUNNER, SeedMixin
from apps.interactive.validation import check_task
from apps.learning.models import Enrollment, LessonProgress
from apps.learning.services import enroll_user
from apps.users.models import CustomUser

CONTENT = load_modules()


class FullCourseMixin:
    @classmethod
    def setUpTestData(cls):
        cls.admin = CustomUser.objects.create_superuser(email='admin@t.uz', username='admin', password='Parol12345!')
        cls.course, _ = seed_course(python_module1)
        for content in CONTENT:
            seed_module(cls.course, content)
        cls.student = CustomUser.objects.create_user(email='s@t.uz', username='s', password='Parol12345!')
        enroll_user(cls.student, cls.course)

    def lesson(self, number):
        return Lesson.objects.get(module__course=self.course, order=number)

    def task(self, lesson_no, section, kind=None):
        qs = Task.objects.filter(lesson=self.lesson(lesson_no), section=section)
        if kind:
            qs = qs.filter(kind=kind)
        return qs.order_by('order', 'id').first()

    def post_json(self, url, data):
        import json
        return self.client.post(url, data=json.dumps(data), content_type='application/json')


class CourseStructureTests(FullCourseMixin, TestCase):
    def test_eleven_modules_and_74_sequential_lessons(self):
        self.assertEqual(len(MODULE_FILES), 10)
        self.assertEqual(len(CONTENT), 10)
        self.assertEqual(self.course.modules.count(), 11)
        self.assertEqual(list(self.course.modules.order_by('order').values_list('order', flat=True)), list(range(1, 12)))
        numbers = list(Lesson.objects.filter(module__course=self.course).order_by('module__order', 'order').values_list('order', flat=True))
        self.assertEqual(numbers, list(range(1, 75)))

    def test_68_new_lessons_with_expected_distribution(self):
        expected = {2: 9, 3: 5, 4: 6, 5: 7, 6: 8, 7: 8, 8: 11, 9: 5, 10: 4, 11: 5}
        for order, count in expected.items():
            module = CourseModule.objects.get(course=self.course, order=order)
            self.assertEqual(module.lessons.count(), count, f"{order}-modul")
        new = Lesson.objects.filter(module__course=self.course, module__order__gte=2).count()
        self.assertEqual(new, 68)
        self.assertEqual(self.course.modules.get(order=1).lessons.count(), 6)

    def test_lesson_number_ranges_match_spec(self):
        ranges = {2: (7, 15), 3: (16, 20), 4: (21, 26), 5: (27, 33), 6: (34, 41), 7: (42, 49), 8: (50, 60), 9: (61, 65), 10: (66, 69), 11: (70, 74)}
        for order, (a, b) in ranges.items():
            nums = list(Lesson.objects.filter(module__course=self.course, module__order=order).order_by('order').values_list('order', flat=True))
            self.assertEqual(nums, list(range(a, b + 1)), f"{order}-modul")

    def test_every_new_lesson_has_all_required_parts(self):
        for lesson in Lesson.objects.filter(module__course=self.course, module__order__gte=2).order_by('order'):
            label = f"{lesson.order}-dars: {lesson.title}"
            tasks = Task.objects.filter(lesson=lesson)
            self.assertTrue(lesson.is_interactive and lesson.is_published, label)
            self.assertTrue(lesson.objective and lesson.concept_list, label)
            self.assertTrue(10 <= lesson.duration_minutes <= 15, label)
            blocks = LessonBlock.objects.filter(lesson=lesson)
            self.assertGreaterEqual(blocks.filter(block_type='text').count(), 1, label)          # nazariya
            self.assertGreaterEqual(blocks.filter(block_type='code', is_runnable=True).count(), 2, label)   # >= 2 kod namunasi
            self.assertGreaterEqual(blocks.filter(block_type='task').count(), 1, label)          # dars ichidagi mashq
            self.assertTrue(2 <= tasks.filter(section=TaskSection.QUIZ).count() <= 3, label)     # mini-test
            assignment = tasks.filter(section=TaskSection.ASSIGNMENT)
            self.assertEqual(assignment.count(), 1, label)
            a = assignment.get()
            self.assertTrue(a.hint and a.partial_solution and a.full_solution and a.tests.exists(), label)
            self.assertEqual(set(tasks.filter(section=TaskSection.PRACTICE).values_list('difficulty', flat=True)), {'easy', 'medium', 'hard'}, label)
            self.assertTrue(tasks.filter(kind='code').exists(), label)                         # mustaqil kod yozish
            for t in tasks:
                self.assertEqual(t.module_id, lesson.module_id)
                self.assertEqual(t.validate_configuration(), [], f"{label}: {t.title}")

    def test_module_assessments_composition(self):
        for order in range(2, 12):
            module = CourseModule.objects.get(course=self.course, order=order)
            assessment = ModuleAssessment.objects.get(module=module, kind=AssessmentKind.MODULE)
            self.assertEqual(assessment.pass_percent, 70)
            kinds = [i.task.kind for i in assessment.items.select_related('task')]
            self.assertGreaterEqual(sum(k in ('single_choice', 'multiple_choice') for k in kinds), 5, f"{order}-modul nazariy")
            self.assertGreaterEqual(kinds.count('predict_output'), 3, f"{order}-modul natija")
            self.assertGreaterEqual(kinds.count('find_error'), 2, f"{order}-modul xato tuzatish")
            project = assessment.items.filter(task__section='project')
            self.assertEqual(project.count(), 1, f"{order}-modul mini-loyiha")
            self.assertEqual(project.get().task.kind, 'code')
            self.assertGreaterEqual(project.get().task.tests.count(), 4)

    def test_reviews_after_modules_3_5_7_and_final(self):
        for order in (3, 5, 7, 11):
            module = CourseModule.objects.get(course=self.course, order=order)
            review = ModuleAssessment.objects.get(module=module, kind=AssessmentKind.REVIEW)
            kinds = [i.task.kind for i in review.items.select_related('task')]
            self.assertGreaterEqual(sum(k in ('single_choice', 'multiple_choice') for k in kinds), 5, review.title)
            self.assertGreaterEqual(kinds.count('predict_output'), 3, review.title)
            self.assertGreaterEqual(kinds.count('find_error'), 2, review.title)
            self.assertGreaterEqual(review.items.filter(task__kind='code').count(), 3, review.title)
        self.assertEqual(ModuleAssessment.objects.filter(module__course=self.course, kind=AssessmentKind.REVIEW).count(), 4)
        titles = list(ModuleAssessment.objects.filter(kind=AssessmentKind.REVIEW).values_list('title', flat=True))
        self.assertTrue(any('Review 1' in t for t in titles) and any('Review 2' in t for t in titles) and any('Review 3' in t for t in titles))
        self.assertTrue(any('Yakuniy' in t for t in titles))
        # Review'lar raqamlangan dars sonini buzmaydi
        self.assertEqual(Lesson.objects.filter(module__course=self.course).count(), 74)

    def test_review_tasks_mix_previous_modules(self):
        review = ModuleAssessment.objects.get(module__course=self.course, module__order=3, kind=AssessmentKind.REVIEW)
        texts = ' '.join(i.task.title + i.task.prompt for i in review.items.select_related('task'))
        self.assertIn('2-modul', texts)
        self.assertIn('3-modul', texts)

    def test_course_info_updated_slug_kept(self):
        # seed testlarda 1-modul kontentidan keladi; to'liq tavsif registry'da
        self.assertEqual(self.course.slug, 'python-0-dan-boshlash')
        self.assertIn('Boshlang', COURSE_FULL['title'])
        self.assertEqual(COURSE_FULL['duration_hours'], 40)

    def test_every_project_is_a_code_task_not_a_text_question(self):
        for order in range(2, 12):
            project = Task.objects.get(module__course=self.course, module__order=order, section='project')
            self.assertEqual(project.kind, 'code')
            self.assertTrue(project.full_solution.strip() and project.partial_solution.strip() and project.hint.strip())
            self.assertGreaterEqual(project.points, 15)


class SeedSafetyTests(FullCourseMixin, TestCase):
    def test_seed_twice_creates_no_duplicates(self):
        before = (Lesson.objects.count(), Task.objects.count(), ModuleAssessment.objects.count(), CourseModule.objects.count())
        for content in CONTENT:
            _, created = seed_module(self.course, content)
            self.assertFalse(created)
        seed_course(python_module1)
        after = (Lesson.objects.count(), Task.objects.count(), ModuleAssessment.objects.count(), CourseModule.objects.count())
        self.assertEqual(before, after)

    def test_module1_and_student_progress_untouched_by_seeding(self):
        m1_tasks = list(Task.objects.filter(module__course=self.course, module__order=1).values_list('id', flat=True))
        task = Task.objects.get(id=m1_tasks[0])
        TaskProgress.objects.create(user=self.student, task=task, attempts_count=2, status='solved')
        enrollment = Enrollment.objects.get(user=self.student, course=self.course)
        LessonProgress.objects.create(enrollment=enrollment, lesson=self.lesson(1))
        for content in CONTENT:
            seed_module(self.course, content)
        self.assertEqual(list(Task.objects.filter(module__course=self.course, module__order=1).values_list('id', flat=True)), m1_tasks)
        self.assertTrue(TaskProgress.objects.get(user=self.student, task=task).is_solved)
        self.assertTrue(LessonProgress.objects.filter(enrollment=enrollment, lesson=self.lesson(1)).exists())

    def test_reset_of_one_module_is_explicit_and_isolated(self):
        before_m3 = list(Task.objects.filter(module__order=3).values_list('id', flat=True))
        seed_module(self.course, CONTENT[0], reset=True)     # faqat 2-modul qayta yaratiladi
        self.assertEqual(list(Task.objects.filter(module__order=3).values_list('id', flat=True)), before_m3)
        self.assertEqual(self.course.modules.count(), 11)


@override_settings(CODE_RUNNER=RUNNER)
class HarnessGradingTests(FullCourseMixin, TestCase):
    """Funksiya topshiriqlari: haqiqiy bajarish + turli argumentlar bilan chaqirish, matn solishtirish emas."""

    def test_harness_marker_ignores_student_prints(self):
        code = build_harness_code('print("hech narsa")\ndef f(x):\n    return x * 2\n', 'print(f(4))')
        self.assertIn('print(f(4))', code)

    def test_function_task_accepts_any_variable_names(self):
        task = self.task(54, TaskSection.ASSIGNMENT)        # katta(a, b)
        good = grade_task(task, {}, 'def katta(p, q):\n    if p >= q:\n        return p\n    return q\n')
        self.assertTrue(good.is_correct, good.test_results)
        good2 = grade_task(task, {}, 'print("modul yuklandi")\ndef katta(x, y):\n    return max(x, y)\n')
        self.assertTrue(good2.is_correct, good2.test_results)

    def test_hardcoded_or_print_only_function_fails(self):
        task = self.task(54, TaskSection.ASSIGNMENT)
        hardcoded = grade_task(task, {}, 'def katta(a, b):\n    return 9\n')
        self.assertFalse(hardcoded.is_correct)
        only_print = grade_task(task, {}, 'def katta(a, b):\n    print(max(a, b))\n')
        self.assertFalse(only_print.is_correct)
        partial = grade_task(task, {}, 'def katta(a, b):\n    return a\n')
        self.assertFalse(partial.is_correct)
        self.assertGreater(partial.score, 0)        # «qisman to'g'ri»
        self.assertLess(partial.score, task.points)

    def test_wrong_signature_gives_readable_failure(self):
        task = self.task(54, TaskSection.ASSIGNMENT)
        res = grade_task(task, {}, 'def boshqa():\n    return 1\n')
        self.assertFalse(res.is_correct)
        self.assertTrue(res.message)

    def test_input_driven_task_tested_with_several_inputs(self):
        task = self.task(15, TaskSection.ASSIGNMENT)        # to'g'ri to'rtburchak yuzi
        self.assertTrue(grade_task(task, {}, 'a = int(input())\nb = int(input())\nprint(a * b)\n').is_correct)
        self.assertFalse(grade_task(task, {}, 'print(24)\n').is_correct)     # oldindan yozilgan javob

    def test_infinite_loop_is_reported_not_crashing(self):
        task = self.task(30, TaskSection.ASSIGNMENT)
        res = grade_task(task, {}, 'while True:\n    pass\n')
        self.assertFalse(res.is_correct)

    def test_runtime_error_reported(self):
        task = self.task(54, TaskSection.ASSIGNMENT)
        res = grade_task(task, {}, 'def katta(a, b):\n    return a / 0\n')
        self.assertFalse(res.is_correct)


@override_settings(CODE_RUNNER=RUNNER)
class StudentJourneyTests(FullCourseMixin, TestCase):
    def lesson_url(self, n):
        return reverse('course_learn_lesson', args=[self.course.slug, self.lesson(n).id])

    def test_new_lesson_page_renders_with_editor_and_tasks(self):
        self.client.force_login(self.student)
        resp = self.client.get(self.lesson_url(7))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertIn("O&#x27;zgaruvchi (Variable) nima?", html)
        self.assertIn('Vazifani bajarish', html)
        self.assertIn('/ 2-modul / 7-dars / Vazifa-1', html)
        self.assertIn('Run', html) if 'Run' in html else self.assertIn('Ishga tushirish', html)
        assignment = self.task(7, TaskSection.ASSIGNMENT)
        self.assertNotIn(assignment.full_solution.splitlines()[0] + '\n' + assignment.full_solution.splitlines()[-1], html)

    def test_every_new_lesson_page_loads_for_enrolled_student(self):
        self.client.force_login(self.student)
        for n in range(7, 75):
            resp = self.client.get(self.lesson_url(n))
            self.assertEqual(resp.status_code, 200, f"{n}-dars")

    def test_all_11_modules_in_progress_dashboard(self):
        self.client.force_login(self.student)
        resp = self.client.get(reverse('interactive_course_progress', args=[self.course.slug]))
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        for order in range(1, 12):
            self.assertIn(f"{order}-modul:", html)
        self.assertIn('Review 1', html)
        self.assertIn('Yakuniy takrorlash', html)
        self.assertEqual(resp.context['summary']['total_lessons'], 74)

    def test_run_check_and_progress_saved(self):
        self.client.force_login(self.student)
        lesson = self.lesson(15)
        run = self.post_json(reverse('interactive_run'), {'code': 'a = int(input())\nprint(a * 2)', 'stdin': '21\n', 'lesson_id': lesson.id}).json()
        self.assertTrue(run['ok'] and run['result']['ok'])
        self.assertEqual(run['result']['stdout'].strip(), '42')

        task = self.task(15, TaskSection.ASSIGNMENT)
        check = reverse('interactive_task_check', args=[task.id])
        wrong = self.post_json(check, {'code': 'print(1)'}).json()
        self.assertFalse(wrong['is_correct'])
        right = self.post_json(check, {'code': task.full_solution}).json()
        self.assertTrue(right['is_correct'])

        progress = TaskProgress.objects.get(user=self.student, task=task)
        self.assertTrue(progress.is_solved)
        self.assertEqual(progress.attempts_count, 2)
        self.assertEqual(TaskAttempt.objects.filter(user=self.student, task=task).count(), 2)
        self.assertEqual(TaskAttempt.objects.filter(user=self.student, task=task, is_correct=True).count(), 1)

    def test_choice_quiz_result_saved_with_explanation(self):
        self.client.force_login(self.student)
        task = self.task(7, TaskSection.QUIZ, 'single_choice')
        right = task.options.get(is_correct=True)
        body = self.post_json(reverse('interactive_task_check', args=[task.id]), {'options': [right.id]}).json()
        self.assertTrue(body['is_correct'])
        self.assertTrue(TaskProgress.objects.get(user=self.student, task=task).is_solved)

    def test_solution_locked_until_attempts(self):
        self.client.force_login(self.student)
        task = self.task(9, TaskSection.ASSIGNMENT)
        resp = self.post_json(reverse('interactive_task_reveal', args=[task.id]), {'what': 'solution'})
        self.assertNotIn('solution', resp.json().get('data', resp.json()))
        self.assertEqual(TaskProgress.objects.filter(user=self.student, task=task, solution_viewed=True).count(), 0)

    def test_code_is_not_lost_on_reload(self):
        self.client.force_login(self.student)
        lesson = self.lesson(52)
        task = self.task(52, TaskSection.ASSIGNMENT)
        resp = self.post_json(reverse('interactive_draft_save'), {'lesson_id': lesson.id, 'key': f'task-{task.id}', 'code': 'def salom(ism, shahar):\n    pass  # yarim yozilgan'})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(CodeDraft.objects.filter(user=self.student, lesson=lesson, key=f'task-{task.id}').exists())
        page = self.client.get(self.lesson_url(52))
        self.assertContains(page, 'yarim yozilgan')

    def test_lesson_completion_persists_and_updates_percent(self):
        self.client.force_login(self.student)
        enrollment = Enrollment.objects.get(user=self.student, course=self.course)
        for n in (7, 8, 9):
            LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=self.lesson(n))
        summary = course_progress_summary(self.student, self.course)
        self.assertEqual(summary['completed_lessons'], 3)
        self.assertEqual(summary['total_lessons'], 74)
        self.assertEqual(summary['percent'], 3 * 100 // 74)
        m2 = next(m for m in summary['modules'] if m['module'].order == 2)
        self.assertEqual(sum(1 for row in m2['lessons'] if row['completed']), 3)
        page = self.client.get(self.lesson_url(7))
        self.assertIn(self.lesson(7).id, page.context['completed_lesson_ids'])

    def test_previous_and_next_lessons_navigable_across_modules(self):
        self.client.force_login(self.student)
        page = self.client.get(self.lesson_url(7))
        self.assertEqual(page.context['prev_lesson'].order, 6)
        self.assertEqual(page.context['next_lesson'].order, 8)
        page = self.client.get(self.lesson_url(15))
        self.assertEqual(page.context['next_lesson'].order, 16)

    def test_module_assessment_and_review_flow(self):
        enrollment = Enrollment.objects.get(user=self.student, course=self.course)
        for lesson in Lesson.objects.filter(module__order__in=(2, 3)):
            LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        self.client.force_login(self.student)
        for module_order, kind in ((2, AssessmentKind.MODULE), (3, AssessmentKind.REVIEW)):
            assessment = ModuleAssessment.objects.get(module__course=self.course, module__order=module_order, kind=kind)
            url = reverse('interactive_assessment', args=[assessment.id])
            self.assertTrue(self.client.get(url).context['status']['can_attempt'])
            data = {}
            for item in assessment.ordered_items():
                t = item.task
                key = f't{t.id}'
                if t.is_choice:
                    data[f'{key}_opt'] = [str(o.id) for o in t.options.filter(is_correct=True)][:1 if t.kind == 'single_choice' else 9]
                elif t.kind == 'predict_output':
                    data[f'{key}_text'] = t.correct_answer
                else:
                    data[f'{key}_code'] = t.full_solution
            resp = self.client.post(url, data)
            attempt = AssessmentAttempt.objects.filter(user=self.student, assessment=assessment).latest('created_at')
            self.assertRedirects(resp, reverse('interactive_assessment_result', args=[attempt.id]))
            self.assertTrue(attempt.passed, f"{assessment.title}: {attempt.percent}%")
            self.assertEqual(attempt.percent, 100)

    def test_assessment_locked_until_module_lessons_done(self):
        self.client.force_login(self.student)
        assessment = ModuleAssessment.objects.get(module__course=self.course, module__order=4, kind=AssessmentKind.MODULE)
        self.assertFalse(self.client.get(reverse('interactive_assessment', args=[assessment.id])).context['status']['unlocked'])

    def test_pass_percent_editable_by_admin_field(self):
        assessment = ModuleAssessment.objects.get(module__course=self.course, module__order=2, kind=AssessmentKind.MODULE)
        assessment.pass_percent = 85
        assessment.save()
        self.assertEqual(ModuleAssessment.objects.get(pk=assessment.pk).pass_percent, 85)


@override_settings(CODE_RUNNER=RUNNER)
class AdminManagementTests(FullCourseMixin, TestCase):
    def test_admin_pages_render_for_new_content(self):
        self.client.force_login(self.admin)
        lesson = self.lesson(52)
        task = self.task(52, TaskSection.ASSIGNMENT)
        module = lesson.module
        for url in (
            reverse('dashboard_course_curriculum', args=[self.course.slug]),
            reverse('dashboard_lesson_interactive', args=[self.course.slug, lesson.id]),
            reverse('dashboard_task_edit', args=[self.course.slug, task.id]),
            reverse('dashboard_module_assessment', args=[self.course.slug, module.id]),
            reverse('dashboard_lesson_edit', args=[self.course.slug, lesson.id]),
        ):
            self.assertEqual(self.client.get(url).status_code, 200, url)

    def test_admin_task_form_shows_harness_field(self):
        self.client.force_login(self.admin)
        task = self.task(52, TaskSection.ASSIGNMENT)
        html = self.client.get(reverse('dashboard_task_edit', args=[self.course.slug, task.id])).content.decode()
        self.assertIn('harness', html)

    def test_admin_can_add_task_and_lesson_without_code(self):
        self.client.force_login(self.admin)
        lesson = self.lesson(10)
        before = Task.objects.filter(lesson=lesson).count()
        create = reverse('dashboard_task_create', args=[self.course.slug, lesson.module_id])
        resp = self.client.get(create + f'?lesson={lesson.id}&section=quiz')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Task.objects.filter(lesson=lesson).count(), before)

    def test_students_cannot_open_admin_pages(self):
        self.client.force_login(self.student)
        lesson = self.lesson(7)
        resp = self.client.get(reverse('dashboard_lesson_interactive', args=[self.course.slug, lesson.id]))
        self.assertNotEqual(resp.status_code, 200)

    def test_task_validation_tool_works_on_harness_tasks(self):
        task = self.task(52, TaskSection.ASSIGNMENT)
        report = check_task(task)
        self.assertTrue(any(level == 'ok' for level, _ in report), report)
        self.assertFalse(any(level == 'error' for level, _ in report), report)

    def test_harness_field_is_part_of_model(self):
        self.assertTrue(TaskTest.objects.exclude(harness='').exists())


@override_settings(CODE_RUNNER=RUNNER)
@unittest.skipUnless(os.environ.get('RUN_SLOW_COURSE_TESTS') == '1', "Sekin test: RUN_SLOW_COURSE_TESTS=1 bilan ishga tushiring")
class AllContentAgainstRealSandboxTests(FullCourseMixin, TestCase):
    """Barcha topshiriqlarning yechimlari testlardan o'tishi, natijalar haqiqiy bajarishga mosligi."""

    def test_every_task_of_every_new_module(self):
        problems = []
        for task in Task.objects.filter(module__course=self.course, module__order__gte=2).prefetch_related('options', 'tests'):
            for level, message in check_task(task):
                if level != 'ok':
                    problems.append(f"{task.logical_name}: {message[:120]}")
        self.assertEqual(problems, [])
