from django.urls import path
from . import views

urlpatterns = [
    path('', views.duel_home_view, name='duel_home'),
    path('send/', views.duel_send_view, name='duel_send'),
    path('ping/', views.duel_ping_view, name='duel_ping'),
    path('<int:duel_id>/', views.duel_room_view, name='duel_room'),
    path('<int:duel_id>/respond/', views.duel_respond_view, name='duel_respond'),
    path('<int:duel_id>/state/', views.duel_state_view, name='duel_state'),
    path('<int:duel_id>/submit/', views.duel_submit_view, name='duel_submit'),
]
