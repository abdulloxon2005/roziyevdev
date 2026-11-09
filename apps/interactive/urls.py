from django.urls import path

from . import views

urlpatterns = [
    path('run/', views.run_code_view, name='interactive_run'),
    path('tasks/<int:task_id>/check/', views.task_check_view, name='interactive_task_check'),
    path('tasks/<int:task_id>/reveal/', views.task_reveal_view, name='interactive_task_reveal'),
    path('tasks/<int:task_id>/attempts/', views.task_attempts_view, name='interactive_task_attempts'),
    path('drafts/', views.draft_save_view, name='interactive_draft_save'),
    path('assessment/<int:assessment_id>/', views.assessment_view, name='interactive_assessment'),
    path('assessment/result/<int:attempt_id>/', views.assessment_result_view, name='interactive_assessment_result'),
    path('progress/', views.my_learning_view, name='interactive_my_learning'),
    path('progress/<slug:slug>/', views.course_progress_view, name='interactive_course_progress'),
]
