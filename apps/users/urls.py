from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterAPIView,
    LoginAPIView,
    CurrentUserProfileAPIView,
    ChangePasswordAPIView,
)

urlpatterns = [
    # REST API endpoints
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('me/', CurrentUserProfileAPIView.as_view(), name='api_profile_me'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='api_change_password'),
]
