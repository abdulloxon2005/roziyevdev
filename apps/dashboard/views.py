from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count, Sum, Q

from apps.courses.models import Course, CourseModule, Lesson, Category
from apps.learning.models import Enrollment, Assignment, AssignmentSubmission, SubmissionStatus
from apps.orders.models import Order, OrderStatus
from apps.users.models import CustomUser
from .forms import CourseForm, CourseModuleForm, LessonForm


def instructor_required(view_func):
    """Faqat o'qituvchi, admin yoki xodim (staff) uchun ruxsat beruvchi dekorator."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")
        user = request.user
        if not (user.is_staff or getattr(user, 'role', '') in ['instructor', 'admin'] or user.is_superuser):
            messages.error(request, "Ushbu bo'limga kirish faqat o'qituvchi va administratorlarga ruxsat etilgan.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ==============================================================================
# DASHBOARD OVERVIEW / BOSH SAHIFA
# ==============================================================================

@instructor_required
def dashboard_index_view(request):
    """Ustoz Studiyasi / Admin bosh sahifasi (Asosiy metrikalar va tezkor havolalar)."""
    courses_qs = Course.objects.all()
    total_courses = courses_qs.count()
    published_courses = courses_qs.filter(is_published=True).count()
    draft_courses = total_courses - published_courses

    total_modules = CourseModule.objects.count()
    total_lessons = Lesson.objects.count()

    total_enrollments = Enrollment.objects.count()
    unique_students = Enrollment.objects.values('user').distinct().count()

    # Vazifalar holati
    all_submissions = AssignmentSubmission.objects.all()
    pending_submissions = all_submissions.filter(status=SubmissionStatus.PENDING).count()
    approved_submissions = all_submissions.filter(status=SubmissionStatus.APPROVED).count()
    total_coins_awarded = all_submissions.aggregate(total=Sum('coins_awarded'))['total'] or 0

    # Savdo va to'lovlar
    all_orders = Order.objects.all()
    paid_orders = all_orders.filter(status=OrderStatus.PAID)
    total_revenue = paid_orders.aggregate(total=Sum('amount'))['total'] or 0

    # Oxirgi kutilayotgan vazifalar
    recent_submissions = AssignmentSubmission.objects.select_related(
        'student', 'assignment__lesson__module__course'
    ).order_by('-created_at')[:6]

    # Oxirgi buyurtmalar
    recent_orders = Order.objects.select_related('user', 'course').order_by('-created_at')[:5]

    # Oxirgi o'quvchilar
    recent_enrollments = Enrollment.objects.select_related('user', 'course').order_by('-created_at')[:5]

    context = {
        'total_courses': total_courses,
        'published_courses': published_courses,
        'draft_courses': draft_courses,
        'total_modules': total_modules,
        'total_lessons': total_lessons,
        'total_enrollments': total_enrollments,
        'unique_students': unique_students,
        'pending_submissions': pending_submissions,
        'approved_submissions': approved_submissions,
        'total_coins_awarded': total_coins_awarded,
        'total_revenue': total_revenue,
        'paid_orders_count': paid_orders.count(),
        'recent_submissions': recent_submissions,
        'recent_orders': recent_orders,
        'recent_enrollments': recent_enrollments,
        'active_menu': 'overview',
    }
    return render(request, 'dashboard/index.html', context)


# ==============================================================================
# KURSLAR BOSHQARUVI (CRUD)
# ==============================================================================

@instructor_required
def dashboard_courses_list_view(request):
    """Barcha kurslar ro'yxati va filtrlash."""
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    status_filter = request.GET.get('status', '').strip()

    qs = Course.objects.select_related('category', 'instructor').annotate(
        modules_count=Count('modules', distinct=True),
        enrolled_students=Count('enrollments', distinct=True)
    ).order_by('-created_at')

    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(short_description__icontains=query))

    if category_slug:
        qs = qs.filter(category__slug=category_slug)

    if status_filter == 'published':
        qs = qs.filter(is_published=True)
    elif status_filter == 'draft':
        qs = qs.filter(is_published=False)

    categories = Category.objects.filter(is_active=True)

    context = {
        'courses': qs,
        'categories': categories,
        'query': query,
        'category_slug': category_slug,
        'status_filter': status_filter,
        'active_menu': 'courses',
    }
    return render(request, 'dashboard/courses_list.html', context)


@instructor_required
def dashboard_course_create_view(request):
    """Yangi kurs yaratish."""
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            if not course.instructor:
                course.instructor = request.user
            course.save()
            messages.success(request, f"«{course.title}» kursi muvaffaqiyatli yaratildi! Endi bo'limlar va darslarni qo'shing.")
            return redirect('dashboard_course_curriculum', slug=course.slug)
    else:
        form = CourseForm()

    context = {
        'form': form,
        'is_create': True,
        'active_menu': 'courses',
    }
    return render(request, 'dashboard/course_form.html', context)


@instructor_required
def dashboard_course_edit_view(request, slug):
    """Mavjud kurs ma'lumotlarini tahrirlash."""
    course = get_object_or_404(Course, slug=slug)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"«{course.title}» kursi ma'lumotlari yangilandi.")
            return redirect('dashboard_course_curriculum', slug=course.slug)
    else:
        form = CourseForm(instance=course)

    context = {
        'form': form,
        'course': course,
        'is_create': False,
        'active_menu': 'courses',
    }
    return render(request, 'dashboard/course_form.html', context)


@instructor_required
@require_POST
def dashboard_course_delete_view(request, slug):
    """Kursni o'chirish."""
    course = get_object_or_404(Course, slug=slug)
    title = course.title
    course.delete()
    messages.warning(request, f"«{title}» kursi butunlay o'chirildi.")
    return redirect('dashboard_courses_list')


# ==============================================================================
# MUNDARIJA, BO'LIMLAR VA DARSLAR BOSHQARUVI (CURRICULUM)
# ==============================================================================

@instructor_required
def dashboard_course_curriculum_view(request, slug):
    """Kurs mundarijasi: modullar va darslarni ko'rish va boshqarish."""
    course = get_object_or_404(
        Course.objects.prefetch_related(
            'modules__lessons__assignment'
        ),
        slug=slug
    )

    module_form = CourseModuleForm()

    context = {
        'course': course,
        'modules': course.modules.all().order_by('order'),
        'module_form': module_form,
        'active_menu': 'courses',
    }
    return render(request, 'dashboard/course_curriculum.html', context)


@instructor_required
@require_POST
def dashboard_module_create_view(request, slug):
    """Kursga yangi modul/bo'lim qo'shish."""
    course = get_object_or_404(Course, slug=slug)
    form = CourseModuleForm(request.POST)
    if form.is_valid():
        module = form.save(commit=False)
        module.course = course
        # Agar order kiritilmagan bo'lsa oxirgi modul tartibidan keyin qo'yish
        if not module.order:
            last = course.modules.order_by('-order').first()
            module.order = (last.order + 1) if last else 1
        module.save()
        messages.success(request, f"«{module.title}» bo'limi qo'shildi.")
    else:
        messages.error(request, "Bo'lim nomini kiritishda xatolik yuz berdi.")
    return redirect('dashboard_course_curriculum', slug=course.slug)


@instructor_required
@require_POST
def dashboard_module_edit_view(request, slug, module_id):
    """Modul/bo'lim nomini yoki tartibini tahrirlash."""
    course = get_object_or_404(Course, slug=slug)
    module = get_object_or_404(CourseModule, id=module_id, course=course)
    form = CourseModuleForm(request.POST, instance=module)
    if form.is_valid():
        form.save()
        messages.success(request, "Bo'lim ma'lumotlari yangilandi.")
    else:
        messages.error(request, "Bo'limni saqlashda xatolik yuz berdi.")
    return redirect('dashboard_course_curriculum', slug=course.slug)


@instructor_required
@require_POST
def dashboard_module_delete_view(request, slug, module_id):
    """Modulni barcha darslari bilan o'chirish."""
    course = get_object_or_404(Course, slug=slug)
    module = get_object_or_404(CourseModule, id=module_id, course=course)
    title = module.title
    module.delete()
    messages.warning(request, f"«{title}» bo'limi o'chirildi.")
    return redirect('dashboard_course_curriculum', slug=course.slug)


# ==============================================================================
# DARS YARATISH VA TAHRIRLASH (VIDEO YUKLASH VA VAZIFA INTEGRATSIYASI)
# ==============================================================================

@instructor_required
def dashboard_lesson_create_view(request, slug, module_id):
    """Kurs bo'limiga yangi dars qo'shish (Video yuklash va Amaliy vazifa biriktirish bilan)."""
    course = get_object_or_404(Course, slug=slug)
    module = get_object_or_404(CourseModule, id=module_id, course=course)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, course=course)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = form.cleaned_data.get('module') or module
            if not lesson.order:
                last_lesson = module.lessons.order_by('-order').first()
                lesson.order = (last_lesson.order + 1) if last_lesson else 1
            lesson.save()
            form.save_assignment(lesson)
            messages.success(request, f"«{lesson.title}» darsi muvaffaqiyatli saqlandi!")
            return redirect('dashboard_course_curriculum', slug=course.slug)
    else:
        last_lesson = module.lessons.order_by('-order').first()
        next_order = (last_lesson.order + 1) if last_lesson else 1
        form = LessonForm(course=course, initial={'module': module, 'order': next_order})

    context = {
        'form': form,
        'course': course,
        'module': module,
        'is_create': True,
        'active_menu': 'courses',
    }
    return render(request, 'dashboard/lesson_form.html', context)


@instructor_required
def dashboard_lesson_edit_view(request, slug, lesson_id):
    """Mavjud darsni tahrirlash (Video faylini almashtirish, vazifani sozlash)."""
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES, instance=lesson, course=course)
        if form.is_valid():
            lesson = form.save()
            form.save_assignment(lesson)
            messages.success(request, f"«{lesson.title}» darsi muvaffaqiyatli yangilandi!")
            return redirect('dashboard_course_curriculum', slug=course.slug)
    else:
        form = LessonForm(instance=lesson, course=course)

    context = {
        'form': form,
        'course': course,
        'module': lesson.module,
        'lesson': lesson,
        'is_create': False,
        'active_menu': 'courses',
    }
    return render(request, 'dashboard/lesson_form.html', context)


@instructor_required
@require_POST
def dashboard_lesson_delete_view(request, slug, lesson_id):
    """Darsni o'chirish."""
    course = get_object_or_404(Course, slug=slug)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)
    title = lesson.title
    lesson.delete()
    messages.warning(request, f"«{title}» darsi o'chirildi.")
    return redirect('dashboard_course_curriculum', slug=course.slug)


# ==============================================================================
# O'QUVCHILAR RO'YXATI VA PROGRESSI
# ==============================================================================

@instructor_required
def dashboard_students_list_view(request):
    """Kurslarga yozilgan o'quvchilar ro'yxati, ularning progressi va tangalari."""
    course_filter = request.GET.get('course', '').strip()
    search_query = request.GET.get('q', '').strip()

    qs = Enrollment.objects.select_related('user__profile', 'course').order_by('-created_at')

    if course_filter and course_filter.isdigit():
        qs = qs.filter(course_id=int(course_filter))

    if search_query:
        qs = qs.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    courses = Course.objects.all().order_by('title')

    context = {
        'enrollments': qs,
        'courses': courses,
        'course_filter': course_filter,
        'search_query': search_query,
        'total_count': qs.count(),
        'active_menu': 'students',
    }
    return render(request, 'dashboard/students_list.html', context)


# ==============================================================================
# BUYURTMALAR VA TO'LOVLAR (ORDERS)
# ==============================================================================

@instructor_required
def dashboard_orders_list_view(request):
    """Platformadagi barcha xaridlar va to'lovlar."""
    status_filter = request.GET.get('status', '').strip()
    search_query = request.GET.get('q', '').strip()

    qs = Order.objects.select_related('user', 'course').order_by('-created_at')

    if status_filter in [OrderStatus.PAID, OrderStatus.PENDING, OrderStatus.FAILED, OrderStatus.CANCELLED]:
        qs = qs.filter(status=status_filter)

    if search_query:
        qs = qs.filter(
            Q(order_number__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(course__title__icontains=search_query)
        )

    # Statistika
    total_revenue = Order.objects.filter(status=OrderStatus.PAID).aggregate(total=Sum('amount'))['total'] or 0
    paid_count = Order.objects.filter(status=OrderStatus.PAID).count()
    pending_count = Order.objects.filter(status=OrderStatus.PENDING).count()

    context = {
        'orders': qs,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_revenue': total_revenue,
        'paid_count': paid_count,
        'pending_count': pending_count,
        'active_menu': 'orders',
    }
    return render(request, 'dashboard/orders_list.html', context)
