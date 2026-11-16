"""Seed kontentni (apps/interactive/content) bazaga yozish."""
from django.db import transaction
from django.utils.text import slugify

from apps.courses.models import Category, Course, CourseModule, Lesson, LessonType
from apps.users.models import CustomUser

from .models import (
    AssessmentItem,
    AssessmentKind,
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
            stdin=t['stdin'], harness=t.get('harness', ''), expected=t['expected'], ignore_case=t['ignore_case'],
            is_hidden=t['hidden'], failure_message=t['failure'],
        )
    return task


def _seed_assessment(module, a, kind, tasks_by_key, log):
    assessment = ModuleAssessment.objects.create(
        module=module, kind=kind, title=a['title'], description=a['description'].strip(),
        pass_percent=a['pass_percent'],
    )
    counters = {}
    for i, tdata in enumerate(a['tasks'], start=1):
        n = counters.get(tdata['section'], 0) + 1
        counters[tdata['section']] = n
        task = _create_task(module, None, tdata, n)
        tasks_by_key[tdata['key']] = task
        AssessmentItem.objects.create(assessment=assessment, task=task, order=i)
    log(f"  {assessment.title}: {assessment.items.count()} ta topshiriq, o'tish foizi {assessment.pass_percent}%")
    return assessment


def _seed_module(course, content, log):
    """Bitta modul (MODULE, LESSONS, ASSESSMENT, ixtiyoriy REVIEWS) ni kursga yozadi."""
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

    _seed_assessment(module, content.ASSESSMENT, AssessmentKind.MODULE, tasks_by_key, log)
    for rv in getattr(content, 'REVIEWS', []):
        _seed_assessment(module, rv, AssessmentKind.REVIEW, tasks_by_key, log)
    return module


def _prepare_course(spec, reset_module_order=None):
    """Kursni (kategoriya, o'qituvchi bilan) yaratadi yoki mavjudini qaytaradi."""
    existing = Course.objects.filter(slug=spec['slug']).first()
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
    course = existing or Course(slug=spec['slug'])
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
    return course


@transaction.atomic
def seed_course(content, reset=False, stdout=None):
    """
    content: COURSE, MODULE, LESSONS, ASSESSMENT atributlariga ega modul (1-modul uchun).
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
    course = _prepare_course(spec)
    _seed_module(course, content, log)
    return course, True


@transaction.atomic
def seed_module(course, content, reset=False, stdout=None):
    """
    Mavjud kursga bitta modul qo'shadi. Shu tartib raqamli modul allaqachon bo'lsa, hech narsa
    o'zgartirilmaydi (dublikat yaratilmaydi, o'quvchi natijalari saqlanadi). reset=True — modulni
    o'chirib qayta yaratadi (shu modul bo'yicha o'quvchi natijalari ham o'chadi!).
    Qaytaradi: (module, created_bool)
    """
    log = (lambda msg: stdout.write(msg)) if stdout else (lambda msg: None)
    order = content.MODULE['order']
    existing = CourseModule.objects.filter(course=course, order=order).first()
    if existing and not reset:
        log(f"{order}-modul allaqachon mavjud («{existing.title}») — o'tkazib yuborildi.")
        return existing, False
    if existing:
        existing.delete()
    return _seed_module(course, content, log), True
