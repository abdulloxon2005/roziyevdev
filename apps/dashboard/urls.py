from django.urls import path
from apps.learning.views import web_submissions_list_view, web_review_submission_view
from . import interactive_views
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
    dashboard_categories_list_view,
    dashboard_category_create_view,
    dashboard_category_edit_view,
    dashboard_category_delete_view,
    dashboard_users_list_view,
    dashboard_user_create_view,
    dashboard_user_edit_view,
    dashboard_user_delete_view,
    dashboard_statistics_view,
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

    # Kategoriyalar boshqaruvi
    path('categories/', dashboard_categories_list_view, name='dashboard_categories_list'),
    path('categories/create/', dashboard_category_create_view, name='dashboard_category_create'),
    path('categories/<int:category_id>/edit/', dashboard_category_edit_view, name='dashboard_category_edit'),
    path('categories/<int:category_id>/delete/', dashboard_category_delete_view, name='dashboard_category_delete'),

    # Foydalanuvchilarni boshqarish
    path('users/', dashboard_users_list_view, name='dashboard_users_list'),
    path('users/create/', dashboard_user_create_view, name='dashboard_user_create'),
    path('users/<int:user_id>/edit/', dashboard_user_edit_view, name='dashboard_user_edit'),
    path('users/<int:user_id>/delete/', dashboard_user_delete_view, name='dashboard_user_delete'),

    # Statistika / Tahlil
    path('statistics/', dashboard_statistics_view, name='dashboard_statistics'),

    # Interaktiv kontent: bloklar, topshiriqlar, modul nazorati, tartiblash
    path('courses/<slug:slug>/modules/<int:module_id>/move/<str:direction>/', interactive_views.module_move_view, name='dashboard_module_move'),
    path('courses/<slug:slug>/lessons/<int:lesson_id>/move/<str:direction>/', interactive_views.lesson_move_view, name='dashboard_lesson_move'),
    path('courses/<slug:slug>/lessons/<int:lesson_id>/interactive/', interactive_views.lesson_interactive_view, name='dashboard_lesson_interactive'),
    path('courses/<slug:slug>/blocks/<int:block_id>/edit/', interactive_views.block_edit_view, name='dashboard_block_edit'),
    path('courses/<slug:slug>/blocks/<int:block_id>/delete/', interactive_views.block_delete_view, name='dashboard_block_delete'),
    path('courses/<slug:slug>/blocks/<int:block_id>/move/<str:direction>/', interactive_views.block_move_view, name='dashboard_block_move'),
    path('courses/<slug:slug>/modules/<int:module_id>/tasks/create/', interactive_views.task_create_view, name='dashboard_task_create'),
    path('courses/<slug:slug>/tasks/<int:task_id>/edit/', interactive_views.task_edit_view, name='dashboard_task_edit'),
    path('courses/<slug:slug>/tasks/<int:task_id>/delete/', interactive_views.task_delete_view, name='dashboard_task_delete'),
    path('courses/<slug:slug>/modules/<int:module_id>/assessment/', interactive_views.module_assessment_view, name='dashboard_module_assessment'),
]
