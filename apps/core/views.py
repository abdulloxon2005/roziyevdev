from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from apps.courses.models import Category, Course
from apps.users.models import CustomUser


def web_home_view(request):
    """
    Asosiy Landing Sahifa ko'rinishi.
    """
    categories = Category.objects.filter(is_active=True).order_by('order')[:6]
    featured_courses = Course.objects.filter(is_published=True, is_featured=True).select_related('category', 'instructor')[:6]
    
    # Agar featured kurslar hali belgilanmagan bo'lsa, oxirgi e'lon qilingan kurslarni olamiz
    if not featured_courses.exists():
        featured_courses = Course.objects.filter(is_published=True).select_related('category', 'instructor')[:6]

    instructor = CustomUser.objects.filter(is_staff=True).first()

    context = {
        'categories': categories,
        'featured_courses': featured_courses,
        'instructor': instructor,
        'stats': {
            'courses_count': Course.objects.filter(is_published=True).count(),
            'students_count': 1450,
            'lessons_count': 180,
            'rating': "4.9",
        }
    }
    return render(request, 'index.html', context)


class HealthCheckAPIView(APIView):
    """
    Tizim holatini tekshirish API'si (Health check).
    """
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        responses={
            200: {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "platform": {"type": "string"},
                    "version": {"type": "string"}
                }
            }
        }
    )
    def get(self, request):
        return Response({
            "status": "online",
            "platform": "RoziyevDev LMS & IT Blog",
            "version": "1.0.0"
        })
