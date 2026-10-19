from django.urls import path
from apps.learning.views import web_submissions_list_view, web_review_submission_view
from .views import (
    dashboard_index_view,
    dashboard_courses_list_view,
    dashboard_course_create_view,
    dashboard_course_edit_view,
    dashboard_course_delete_view,
    dashboard_course_curriculum_view,
    dashboard_module_create_view,
    dashboard_module_edit_view,
    dashboard_module_delete_view,
    dashboard_lesson_create_view,
    dashboard_lesson_edit_view,
    dashboard_lesson_delete_view,
    dashboard_students_list_view,
    dashboard_orders_list_view,
)

urlpatterns = [
    # Bosh sahifa
    path('', dashboard_index_view, name='dashboard_index'),

    # Kurslar boshqaruvi
    path('courses/', dashboard_courses_list_view, name='dashboard_courses_list'),
    path('courses/create/', dashboard_course_create_view, name='dashboard_course_create'),
    path('courses/<slug:slug>/edit/', dashboard_course_edit_view, name='dashboard_course_edit'),
    path('courses/<slug:slug>/delete/', dashboard_course_delete_view, name='dashboard_course_delete'),

    # Mundarija (Modullar va Darslar)
    path('courses/<slug:slug>/curriculum/', dashboard_course_curriculum_view, name='dashboard_course_curriculum'),
    path('courses/<slug:slug>/modules/add/', dashboard_module_create_view, name='dashboard_module_create'),
    path('courses/<slug:slug>/modules/<int:module_id>/edit/', dashboard_module_edit_view, name='dashboard_module_edit'),
    path('courses/<slug:slug>/modules/<int:module_id>/delete/', dashboard_module_delete_view, name='dashboard_module_delete'),

    # Darslar (Video yuklash & Vazifalar)
    path('courses/<slug:slug>/modules/<int:module_id>/lessons/create/', dashboard_lesson_create_view, name='dashboard_lesson_create'),
    path('courses/<slug:slug>/lessons/<int:lesson_id>/edit/', dashboard_lesson_edit_view, name='dashboard_lesson_edit'),
    path('courses/<slug:slug>/lessons/<int:lesson_id>/delete/', dashboard_lesson_delete_view, name='dashboard_lesson_delete'),

    # O'quvchilar va buyurtmalar
    path('students/', dashboard_students_list_view, name='dashboard_students_list'),
    path('orders/', dashboard_orders_list_view, name='dashboard_orders_list'),

    # Vazifalarni tekshirish (Instructor Review Desk)
    path('reviews/', web_submissions_list_view, name='dashboard_reviews_list'),
    path('reviews/<int:submission_id>/', web_review_submission_view, name='dashboard_review_detail'),
]
