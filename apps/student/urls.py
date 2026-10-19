from django.urls import path
from .views import (
    student_dashboard_view,
    student_assignments_hub_view,
    student_assignment_solve_view,
    student_leaderboard_view,
    student_contests_list_view,
    student_contest_detail_view,
    student_contest_submit_view,
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
    student_roadmap_view,
)

urlpatterns = [
    # Bosh sahifa
    path('', student_dashboard_view, name='student_dashboard'),

    # Vazifalar studiyasi
    path('assignments/', student_assignments_hub_view, name='student_assignments_hub'),
    path('assignments/<int:assignment_id>/solve/', student_assignment_solve_view, name='student_assignment_solve'),

    # Kurs Reytingi
    path('leaderboard/', student_leaderboard_view, name='student_leaderboard'),

    # Musobaqalar
    path('contests/', student_contests_list_view, name='student_contests'),
    path('contests/<slug:slug>/', student_contest_detail_view, name='student_contest_detail'),
    path('contests/<slug:contest_slug>/problems/<int:problem_id>/submit/', student_contest_submit_view, name='student_contest_submit'),

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

    # Dasturchi Yo'li
    path('roadmap/', student_roadmap_view, name='student_roadmap'),
    path('roadmap/<slug:track_slug>/', student_roadmap_view, name='student_roadmap_track'),
]

