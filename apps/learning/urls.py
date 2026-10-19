from django.urls import path
from .views import (
    web_enroll_action_view,
    web_course_learn_view,
    web_toggle_lesson_view,
    web_submit_assignment_view,
    web_submissions_list_view,
    web_review_submission_view,
)

urlpatterns = [
    # Web sahifalar
    path('learn/<slug:slug>/', web_course_learn_view, name='course_learn'),
    path('learn/<slug:slug>/lesson/<int:lesson_id>/', web_course_learn_view, name='course_learn_lesson'),
    path('enroll/<slug:slug>/', web_enroll_action_view, name='enroll_course'),
    path('enroll-action/<slug:slug>/', web_enroll_action_view, name='enroll_action'),
    path('toggle-lesson/<int:lesson_id>/', web_toggle_lesson_view, name='toggle_lesson_progress'),
    path('lessons/<int:lesson_id>/toggle-view/', web_toggle_lesson_view, name='toggle_lesson'),
    path('assignments/<int:assignment_id>/submit/', web_submit_assignment_view, name='submit_assignment'),
    path('dashboard/reviews/', web_submissions_list_view, name='submissions_review_list'),
    path('dashboard/reviews/<int:submission_id>/', web_review_submission_view, name='submission_review_detail'),
]
