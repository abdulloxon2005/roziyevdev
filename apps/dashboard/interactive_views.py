"""
Ustoz Studiyasi: interaktiv dars kontentini boshqarish.

Admin/o'qituvchi kod yozmasdan:
  * darsga nazariya bloklari, kod misollari, rasm/video va dars ichidagi mashqlarni qo'shadi;
  * topshiriqlar (test, natijani aniqlash, bo'sh joy, xatoni tuzatish, kod yozish), ularning
    javob variantlari va avtomatik testlarini boshqaradi;
  * modul yakuniy nazoratini sozlaydi (savollar, o'tish foizi);
  * modul va darslar tartibini o'zgartiradi.
Ruxsat server tomonida `instructor_required` orqali tekshiriladi (talabalar kira olmaydi).
"""
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.courses.models import Course, CourseModule, Lesson
from apps.interactive.models import (
    AssessmentItem,
    LessonBlock,
    ModuleAssessment,
    Task,
    TaskSection,
)
from apps.interactive.validation import check_task

from .interactive_forms import (
    LessonBlockForm,
    ModuleAssessmentForm,
    TaskForm,
    TaskOptionFormSet,
    TaskTestFormSet,
    style_formset,
)
from .views import instructor_required


def _form_errors(form):
    return "; ".join(f"{form.fields[f].label if f in form.fields else f}: {', '.join(e)}" for f, e in form.errors.items())


def _swap_order(queryset, obj, direction):
    """Tartib raqamlarini 1..n qilib normallashtiradi va obyektni qo'shnisi bilan almashtiradi."""
    items = list(queryset)
    for i, item in enumerate(items, start=1):
        if item.order != i:
            item.order = i
            item.save(update_fields=['order'])
    idx = next((i for i, it in enumerate(items) if it.pk == obj.pk), None)
    if idx is None:
        return
    target = idx - 1 if direction == 'up' else idx + 1
    if 0 <= target < len(items):
        a, b = items[idx], items[target]
        a.order, b.order = b.order, a.order
        a.save(update_fields=['order'])
        b.save(update_fields=['order'])


# ==============================================================================
# MODUL VA DARS TARTIBI
# ==============================================================================

@instructor_required
@require_POST
def module_move_view(request, slug, module_id, direction):
    course = get_object_or_404(Course, slug=slug)
    module = get_object_or_404(CourseModule, id=module_id, course=course)
    with transaction.atomic():
        _swap_order(course.modules.order_by('order', 'id'), module, direction)
    return redirect('dashboard_course_curriculum', slug=course.slug)


@instructor_required
@require_POST
def lesson_move_view(request, slug, lesson_id, direction):
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    with transaction.atomic():
        _swap_order(lesson.module.lessons.order_by('order', 'id'), lesson, direction)
    return redirect('dashboard_course_curriculum', slug=course.slug)


# ==============================================================================
# DARS KONTENTI (BLOKLAR) VA TOPSHIRIQLAR RO'YXATI
# ==============================================================================

@instructor_required
def lesson_interactive_view(request, slug, lesson_id):
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson.objects.select_related('module'), id=lesson_id, module__course=course)

    if request.method == 'POST':
        form = LessonBlockForm(request.POST, request.FILES, lesson=lesson)
        if form.is_valid():
            block = form.save(commit=False)
            block.lesson = lesson
            if not block.order:
                last = lesson.blocks.order_by('-order').first()
                block.order = (last.order + 1) if last else 1
            block.save()
            messages.success(request, "Blok qo'shildi.")
            return redirect(f"{request.path}#block-{block.id}")
        messages.error(request, "Blokni saqlab bo'lmadi: " + _form_errors(form))
    else:
        last = lesson.blocks.order_by('-order').first()
        form = LessonBlockForm(lesson=lesson, initial={'order': (last.order + 1) if last else 1})

    blocks = [
        {'obj': b, 'form': LessonBlockForm(instance=b, lesson=lesson, prefix=f"b{b.id}")}
        for b in lesson.blocks.select_related('task').order_by('order', 'id')
    ]
    tasks = list(
        Task.objects.filter(lesson=lesson).prefetch_related('options', 'tests').order_by('section', 'order', 'id')
    )
    sections = []
    for value, label in TaskSection.choices:
        items = [{'task': t, 'problems': t.validate_configuration()} for t in tasks if t.section == value]
        if items:
            sections.append({'value': value, 'label': label, 'items': items})

    return render(request, 'dashboard/lesson_interactive.html', {
        'course': course,
        'lesson': lesson,
        'module': lesson.module,
        'blocks': blocks,
        'new_block_form': form,
        'task_sections': sections,
        'section_choices': TaskSection.choices,
        'active_menu': 'courses',
    })


@instructor_required
@require_POST
def block_edit_view(request, slug, block_id):
    block = get_object_or_404(LessonBlock.objects.select_related('lesson__module__course'), id=block_id, lesson__module__course__slug=slug)
    form = LessonBlockForm(request.POST, request.FILES, instance=block, lesson=block.lesson, prefix=f"b{block.id}")
    if form.is_valid():
        form.save()
        messages.success(request, "Blok yangilandi.")
    else:
        messages.error(request, "Blokni saqlab bo'lmadi: " + _form_errors(form))
    return redirect(f"/dashboard/courses/{slug}/lessons/{block.lesson_id}/interactive/#block-{block.id}")


@instructor_required
@require_POST
def block_delete_view(request, slug, block_id):
    block = get_object_or_404(LessonBlock, id=block_id, lesson__module__course__slug=slug)
    lesson_id = block.lesson_id
    block.delete()
    messages.warning(request, "Blok o'chirildi.")
    return redirect('dashboard_lesson_interactive', slug=slug, lesson_id=lesson_id)


@instructor_required
@require_POST
def block_move_view(request, slug, block_id, direction):
    block = get_object_or_404(LessonBlock, id=block_id, lesson__module__course__slug=slug)
    with transaction.atomic():
        _swap_order(block.lesson.blocks.order_by('order', 'id'), block, direction)
    return redirect(f"/dashboard/courses/{slug}/lessons/{block.lesson_id}/interactive/#block-{block.id}")


# ==============================================================================
# TOPSHIRIQ YARATISH / TAHRIRLASH (variantlar va avtomatik testlar bilan)
# ==============================================================================

def _task_form_page(request, course, module, task, initial=None):
    is_new = task.pk is None
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, module=module)
        options = style_formset(TaskOptionFormSet(request.POST, instance=task, prefix='opt'))
        tests = style_formset(TaskTestFormSet(request.POST, instance=task, prefix='test'))
        if form.is_valid() and options.is_valid() and tests.is_valid():
            with transaction.atomic():
                task = form.save(commit=False)
                task.module = module
                task.save()
                options.instance = task
                tests.instance = task
                options.save()
                tests.save()
            report = check_task(task)
            errors = [m for lvl, m in report if lvl == 'error']
            if errors:
                messages.warning(request, "Topshiriq saqlandi, lekin tekshiruvda muammolar bor: " + " | ".join(errors))
            else:
                messages.success(request, f"«{task.title}» saqlandi. " + " ".join(m for lvl, m in report if lvl == 'ok'))
            if request.POST.get('_continue') or errors:
                return redirect('dashboard_task_edit', slug=course.slug, task_id=task.id)
            if task.lesson_id:
                return redirect('dashboard_lesson_interactive', slug=course.slug, lesson_id=task.lesson_id)
            return redirect('dashboard_module_assessment', slug=course.slug, module_id=module.id)
        messages.error(request, "Formada xatolar bor. Iltimos, tekshiring.")
    else:
        form = TaskForm(instance=task, module=module, initial=initial or {})
        options = style_formset(TaskOptionFormSet(instance=task, prefix='opt'))
        tests = style_formset(TaskTestFormSet(instance=task, prefix='test'))

    return render(request, 'dashboard/task_form.html', {
        'course': course,
        'module': module,
        'task': task if not is_new else None,
        'form': form,
        'options': options,
        'tests': tests,
        'report': check_task(task) if not is_new and request.method == 'GET' else [],
        'active_menu': 'courses',
    })


@instructor_required
def task_create_view(request, slug, module_id):
    course = get_object_or_404(Course, slug=slug)
    module = get_object_or_404(CourseModule, id=module_id, course=course)
    initial = {}
    lesson_id = request.GET.get('lesson')
    if lesson_id and lesson_id.isdigit():
        lesson = module.lessons.filter(id=int(lesson_id)).first()
        if lesson:
            initial['lesson'] = lesson
            last = Task.objects.filter(lesson=lesson).order_by('-order').first()
            initial['order'] = (last.order + 1) if last else 1
    section = request.GET.get('section')
    if section in dict(TaskSection.choices):
        initial['section'] = section
        if section in (TaskSection.ASSIGNMENT, TaskSection.PROJECT):
            initial['kind'] = 'code'
            initial['points'] = 10
    return _task_form_page(request, course, module, Task(module=module), initial)


@instructor_required
def task_edit_view(request, slug, task_id):
    course = get_object_or_404(Course, slug=slug)
    task = get_object_or_404(Task.objects.select_related('module', 'lesson'), id=task_id, module__course=course)
    return _task_form_page(request, course, task.module, task)


@instructor_required
@require_POST
def task_delete_view(request, slug, task_id):
    task = get_object_or_404(Task, id=task_id, module__course__slug=slug)
    lesson_id, module_id, title = task.lesson_id, task.module_id, task.title
    task.delete()
    messages.warning(request, f"«{title}» topshirig'i o'chirildi (barcha urinishlar bilan).")
    if lesson_id:
        return redirect('dashboard_lesson_interactive', slug=slug, lesson_id=lesson_id)
    return redirect('dashboard_module_assessment', slug=slug, module_id=module_id)


# ==============================================================================
# MODUL YAKUNIY NAZORATI
# ==============================================================================

@instructor_required
def module_assessment_view(request, slug, module_id):
    course = get_object_or_404(Course, slug=slug)
    module = get_object_or_404(CourseModule, id=module_id, course=course)
    assessment = ModuleAssessment.objects.filter(module=module).first()
    candidate_tasks = list(
        Task.objects.filter(module=module).select_related('lesson').order_by('lesson__order', 'section', 'order', 'id')
    )

    if request.method == 'POST':
        form = ModuleAssessmentForm(request.POST, instance=assessment or ModuleAssessment(module=module))
        if form.is_valid():
            valid_ids = {t.id for t in candidate_tasks}
            selected = []
            for raw in request.POST.getlist('tasks'):
                if raw.isdigit() and int(raw) in valid_ids:
                    order_raw = request.POST.get(f"order_{raw}", '')
                    selected.append((int(raw), int(order_raw) if order_raw.isdigit() else 999))
            with transaction.atomic():
                assessment = form.save(commit=False)
                assessment.module = module
                assessment.save()
                AssessmentItem.objects.filter(assessment=assessment).exclude(task_id__in=[s[0] for s in selected]).delete()
                for task_id, order in selected:
                    AssessmentItem.objects.update_or_create(assessment=assessment, task_id=task_id, defaults={'order': order})
            messages.success(request, f"Nazorat saqlandi: {len(selected)} ta topshiriq, o'tish foizi {assessment.pass_percent}%.")
            return redirect('dashboard_module_assessment', slug=slug, module_id=module.id)
        messages.error(request, "Formada xatolar bor: " + _form_errors(form))
    else:
        form = ModuleAssessmentForm(instance=assessment, initial=None if assessment else {
            'title': f"{module.order}-modul yakuniy nazorati", 'pass_percent': 70,
        })

    items = {i.task_id: i.order for i in assessment.items.all()} if assessment else {}
    rows = [{'task': t, 'selected': t.id in items, 'order': items.get(t.id, '')} for t in candidate_tasks]
    total_points = sum(t.points for t in candidate_tasks if t.id in items)
    return render(request, 'dashboard/module_assessment.html', {
        'course': course,
        'module': module,
        'assessment': assessment,
        'form': form,
        'rows': rows,
        'total_points': total_points,
        'active_menu': 'courses',
    })
