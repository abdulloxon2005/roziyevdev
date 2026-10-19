from django.urls import path
from .views import (
    BlogCategoryListAPIView,
    PostListAPIView,
    PostDetailAPIView,
    CommentCreateAPIView,
)

urlpatterns = [
    # REST API endpoints
    path('categories/', BlogCategoryListAPIView.as_view(), name='api_blog_categories'),
    path('posts/', PostListAPIView.as_view(), name='api_post_list'),
    path('posts/<slug:slug>/', PostDetailAPIView.as_view(), name='api_post_detail'),
    path('comments/', CommentCreateAPIView.as_view(), name='api_comment_create'),

    # Eski /api/ prefiksi bilan moslik (Backwards compatibility)
    path('api/categories/', BlogCategoryListAPIView.as_view()),
    path('api/posts/', PostListAPIView.as_view()),
    path('api/posts/<slug:slug>/', PostDetailAPIView.as_view()),
    path('api/comments/', CommentCreateAPIView.as_view()),
]
