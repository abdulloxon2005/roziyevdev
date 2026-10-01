from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import generics, permissions, filters
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Category, Course
from .serializers import (
    CategorySerializer,
    CourseListSerializer,
    CourseDetailSerializer,
)


# ==============================================================================
# REST API VIEWS
# ==============================================================================

class CategoryListAPIView(generics.ListAPIView):
    """
    Barcha faol kurs kategoriyalari ro'yxati (Mobil dasturlash, Algoritmlar, Ma'lumotlar bazasi va h.k.).
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class CourseListAPIView(generics.ListAPIView):
    """
    Kurslar ro'yxati API'si.
    Qidiruv va toifalar bo'yicha filtrlash imkoniyatlari mavjud.
    """
    serializer_class = CourseListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'short_description', 'description']

    def get_queryset(self):
        queryset = Course.objects.filter(is_published=True).select_related('category', 'instructor')
        
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)

        is_free = self.request.query_params.get('is_free')
        if is_free is not None:
            if is_free.lower() in ['true', '1']:
                queryset = queryset.filter(is_free=True)
            elif is_free.lower() in ['false', '0']:
                queryset = queryset.filter(is_free=False)

        featured = self.request.query_params.get('featured')
        if featured is not None and featured.lower() in ['true', '1']:
            queryset = queryset.filter(is_featured=True)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(name='category', description='Kategoriya slug bo\'yicha filter', required=False, type=str),
            OpenApiParameter(name='level', description='Daraja (beginner, intermediate, advanced)', required=False, type=str),
            OpenApiParameter(name='is_free', description='Bepul kurslar (true/false)', required=False, type=bool),
            OpenApiParameter(name='featured', description='Tavsiya etilgan kurslar (true/false)', required=False, type=bool),
            OpenApiParameter(name='search', description='Kurs nomi bo\'yicha qidiruv', required=False, type=str),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CourseDetailAPIView(generics.RetrieveAPIView):
    """
    Kursning to'liq ma'lumotlarini slug bo'yicha olish API'si (Mundarija va darslar bilan).
    """
    queryset = Course.objects.filter(is_published=True).prefetch_related('modules__lessons')
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


# ==============================================================================
# WEB TEMPLATE VIEWS
# ==============================================================================

def web_course_list_view(request):
    categories = Category.objects.filter(is_active=True)
    courses = Course.objects.filter(is_published=True).select_related('category', 'instructor')

    # Qidiruv
    search_query = request.GET.get('search', '').strip()
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(short_description__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Kategoriya bo'yicha filter
    selected_category = request.GET.get('category', '').strip()
    if selected_category:
        courses = courses.filter(category__slug=selected_category)

    # Daraja bo'yicha filter
    selected_level = request.GET.get('level', '').strip()
    if selected_level:
        courses = courses.filter(level=selected_level)

    # Narx bo'yicha filter
    price_filter = request.GET.get('price', '').strip()
    if price_filter == 'free':
        courses = courses.filter(is_free=True)
    elif price_filter == 'paid':
        courses = courses.filter(is_free=False)

    context = {
        'categories': categories,
        'courses': courses,
        'selected_category': selected_category,
        'selected_level': selected_level,
        'price_filter': price_filter,
        'search_query': search_query,
    }
    return render(request, 'courses/list.html', context)


def web_course_detail_view(request, slug):
    course = get_object_or_404(
        Course.objects.prefetch_related('modules__lessons', 'category', 'instructor'),
        slug=slug,
        is_published=True
    )
    related_courses = Course.objects.filter(
        category=course.category,
        is_published=True
    ).exclude(id=course.id)[:3]

    context = {
        'course': course,
        'related_courses': related_courses,
    }
    return render(request, 'courses/detail.html', context)
