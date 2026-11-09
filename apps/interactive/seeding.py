"""Seed kontentni (apps/interactive/content) bazaga yozish."""
from django.db import transaction
from django.utils.text import slugify

from apps.courses.models import Category, Course, CourseModule, Lesson, LessonType
from apps.users.models import CustomUser

from .models import (
    AssessmentItem,
    BlockType,
    LessonBlock,
    ModuleAssessment,
    Task,
    TaskOption,
    TaskTest,
)


def _create_task(module, lesson, data, order):
    task = Task.objects.create(
        module=module,
        lesson=lesson,
        section=data['section'],
        kind=data['kind'],
        difficulty=data['difficulty'],
        order=order,
        title=data['title'],
        prompt=data['prompt'],
        code_snippet=data['code_snippet'],
        starter_code=data['starter_code'],
        expected_output_example=data['expected_output_example'],
        correct_answer=data['correct_answer'],
        hint=data['hint'],
        partial_solution=data['partial_solution'],
        full_solution=data['full_solution'],
        explanation=data['explanation'],
        points=data['points'],
        solution_unlock_attempts=data['solution_unlock_attempts'],
    )
    for i, (text, correct, feedback) in enumerate(data['options'], start=1):
        TaskOption.objects.create(task=task, order=i, text=text, is_correct=correct, feedback=feedback)
    for i, t in enumerate(data['tests'], start=1):
        TaskTest.objects.create(
            task=task, order=i, description=t['description'] or t['check'], check_type=t['check'],
            stdin=t['stdin'], expected=t['expected'], ignore_case=t['ignore_case'],
            is_hidden=t['hidden'], failure_message=t['failure'],
        )
    return task


@transaction.atomic
def seed_course(content, reset=False, stdout=None):
    """
    content: COURSE, MODULE, LESSONS, ASSESSMENT atributlariga ega modul.
    Qaytaradi: (course, created_bool)
    """
    log = (lambda msg: stdout.write(msg)) if stdout else (lambda msg: None)
    spec = content.COURSE
    existing = Course.objects.filter(slug=spec['slug']).first()
    if existing and not reset:
        log(f"Kurs allaqachon mavjud: «{existing.title}». Admin tahrirlarini saqlash uchun o'tkazib yuborildi (--reset bilan qayta yaratish mumkin).")
        return existing, False
    if existing and reset:
        existing.modules.filter(order=content.MODULE['order']).delete()
        course = existing
    else:
        course = None

    # Avval mavjud kategoriyani qayta ishlatamiz (masalan, «Backend & Python Dasturlash»), dublikat yaratmaymiz
    category = (
        Category.objects.filter(name__iexact=spec['category']).first()
        or Category.objects.filter(name__icontains='python').order_by('order', 'id').first()
    )
    if category is None:
        category = Category.objects.create(
            name=spec['category'], slug=slugify(spec['category']) or 'python', icon='fa-brands fa-python',
        )
    instructor = (
        CustomUser.objects.filter(is_superuser=True).order_by('id').first()
        or CustomUser.objects.filter(role__in=['admin', 'instructor']).order_by('id').first()
    )
    if course is None:
        course = Course(slug=spec['slug'])
    course.title = spec['title']
    course.category = category
    course.instructor = course.instructor or instructor
    course.short_description = spec['short_description']
    course.description = spec['description']
    course.level = spec['level']
    course.price = 0
    course.is_free = True
    course.duration_hours = spec['duration_hours']
    course.what_you_will_learn = spec['what_you_will_learn']
    course.requirements = spec['requirements']
    course.is_published = True
    course.is_archived = False
    course.save()

    m = content.MODULE
    module = CourseModule.objects.create(
        course=course, order=m['order'], title=m['title'], description=m['description'], is_published=True,
    )

    tasks_by_key = {}
    for ldata in content.LESSONS:
        lesson = Lesson.objects.create(
            module=module,
            title=ldata['title'],
            lesson_type=LessonType.INTERACTIVE,
            duration_minutes=ldata['duration'],
            objective=ldata['objective'],
            key_concepts='\n'.join(ldata['concepts']),
            order=ldata['order'],
            is_preview=ldata['order'] == 1,
            is_published=True,
        )
        section_counters = {}
        for tdata in ldata['tasks']:
            n = section_counters.get(tdata['section'], 0) + 1
            section_counters[tdata['section']] = n
            tasks_by_key[tdata['key']] = _create_task(module, lesson, tdata, n)

        for i, b in enumerate(ldata['blocks'], start=1):
            block = LessonBlock(lesson=lesson, order=i)
            if b['type'] == 'text':
                block.block_type, block.title, block.body = BlockType.TEXT, b['title'], b['body']
            elif b['type'] == 'callout':
                block.block_type, block.title, block.body, block.callout_style = BlockType.CALLOUT, b['title'], b['body'], b['style']
            elif b['type'] == 'code':
                block.block_type, block.title, block.code, block.body, block.is_runnable = (
                    BlockType.CODE, b['title'], b['code'], b['body'], b['runnable'])
            elif b['type'] == 'task':
                block.block_type = BlockType.TASK
                block.task = tasks_by_key[b['task']]
            block.save()
        log(f"  {lesson.order}-dars: {lesson.title} — {lesson.blocks.count()} blok, {lesson.tasks.count()} topshiriq")

    a = content.ASSESSMENT
    assessment = ModuleAssessment.objects.create(
        module=module, title=a['title'], description=a['description'].strip(), pass_percent=a['pass_percent'],
    )
    counters = {}
    for i, tdata in enumerate(a['tasks'], start=1):
        n = counters.get(tdata['section'], 0) + 1
        counters[tdata['section']] = n
        task = _create_task(module, None, tdata, n)
        tasks_by_key[tdata['key']] = task
        AssessmentItem.objects.create(assessment=assessment, task=task, order=i)
    log(f"  Modul nazorati: {assessment.items.count()} ta topshiriq, o'tish foizi {assessment.pass_percent}%")
    return course, True
