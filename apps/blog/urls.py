from django.urls import path
from .views import (
    web_blog_list_view,
    web_blog_detail_view,
    web_post_comment_view,
)

urlpatterns = [
    # Web sahifalar
    path('', web_blog_list_view, name='blog_list'),
    path('<slug:slug>/', web_blog_detail_view, name='blog_detail'),
    path('<slug:slug>/comment/', web_post_comment_view, name='blog_comment'),
]
