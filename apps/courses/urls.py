from django.urls import path
from .views import (
    CategoryListAPIView,
    CourseListAPIView,
    CourseDetailAPIView,
)

urlpatterns = [
    # REST API endpoints
    path('categories/', CategoryListAPIView.as_view(), name='api_category_list'),
    path('', CourseListAPIView.as_view(), name='api_course_list'),
    path('<slug:slug>/', CourseDetailAPIView.as_view(), name='api_course_detail'),
]
