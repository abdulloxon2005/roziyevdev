from django.urls import path
from .views import (
    MyEnrollmentsAPIView,
    EnrollCourseAPIView,
    ToggleLessonAPIView,
)

urlpatterns = [
    path('my-courses/', MyEnrollmentsAPIView.as_view(), name='api_my_enrollments'),
    path('enroll/<slug:slug>/', EnrollCourseAPIView.as_view(), name='api_enroll_course'),
    path('lessons/<int:lesson_id>/toggle/', ToggleLessonAPIView.as_view(), name='api_toggle_lesson'),
]
