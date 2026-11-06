from django.urls import path
from .views import (
    student_dashboard_view,
    student_home_view,
    student_about_view,
    student_assignments_hub_view,
    student_assignment_solve_view,
    student_projects_view,
    student_project_create_view,
    student_project_ide_view,
    student_project_file_get_view,
    student_project_file_save_view,
    student_project_file_create_view,
    student_project_file_delete_view,
    student_project_submit_view,
    student_project_download_zip_view,
    student_project_delete_view,
    student_project_run_code_view,
    student_project_like_view,
)

urlpatterns = [
    # Bosh sahifa
    path('', student_home_view, name='student_home'),
    path('dashboard/', student_dashboard_view, name='student_dashboard'),
    path('about/', student_about_view, name='student_about'),

    # Vazifalar studiyasi
    path('assignments/', student_assignments_hub_view, name='student_assignments_hub'),
    path('assignments/<int:assignment_id>/solve/', student_assignment_solve_view, name='student_assignment_solve'),



    # Loyihalar va In-Browser IDE
    path('projects/', student_projects_view, name='student_projects'),
    path('projects/create/', student_project_create_view, name='student_project_create'),
    path('projects/<int:project_id>/ide/', student_project_ide_view, name='student_project_ide'),
    path('projects/<int:project_id>/submit/', student_project_submit_view, name='student_project_submit'),
    path('projects/<int:project_id>/download/', student_project_download_zip_view, name='student_project_download_zip'),
    path('projects/<int:project_id>/delete/', student_project_delete_view, name='student_project_delete'),
    path('projects/<int:project_id>/run/', student_project_run_code_view, name='student_project_run'),
    path('projects/<int:project_id>/like/', student_project_like_view, name='student_project_like'),

    # Loyiha fayllari AJAX
    path('projects/<int:project_id>/files/create/', student_project_file_create_view, name='student_project_file_create'),
    path('projects/<int:project_id>/files/<int:file_id>/', student_project_file_get_view, name='student_project_file_get'),
    path('projects/<int:project_id>/files/<int:file_id>/save/', student_project_file_save_view, name='student_project_file_save'),
    path('projects/<int:project_id>/files/<int:file_id>/delete/', student_project_file_delete_view, name='student_project_file_delete'),

]

