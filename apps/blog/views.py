from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.contrib import messages
from django.views.decorators.http import require_POST
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import BlogCategory, Tag, Post, Comment
from .serializers import (
    BlogCategorySerializer,
    TagSerializer,
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
)


# ==============================================================================
# WEB VIEWS
# ==============================================================================

def web_blog_list_view(request):
    """Blog maqolalari ro'yxati (qidiruv, kategoriya va teg filtrlari bilan)."""
    posts = Post.objects.filter(is_published=True).select_related('author__profile', 'category').prefetch_related('tags')

    # Qidiruv
    search_query = request.GET.get('search', '').strip()
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    # Kategoriya bo'yicha filter
    category_slug = request.GET.get('category', '').strip()
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(BlogCategory, slug=category_slug)
        posts = posts.filter(category=selected_category)

    # Teg bo'yicha filter
    tag_slug = request.GET.get('tag', '').strip()
    selected_tag = None
    if tag_slug:
        selected_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=selected_tag)

    # Sahifalash (Pagination)
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = BlogCategory.objects.all()
    popular_tags = Tag.objects.all()[:15]
    featured_posts = Post.objects.filter(is_published=True).order_by('-views_count')[:3]

    context = {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'categories': categories,
        'popular_tags': popular_tags,
        'featured_posts': featured_posts,
        'search_query': search_query,
        'selected_category': selected_category,
        'selected_tag': selected_tag,
    }
    return render(request, 'blog/list.html', context)


def web_blog_detail_view(request, slug):
    """Maqola to'liq ko'rinishi va izohlar."""
    post = get_object_or_404(
        Post.objects.select_related('author__profile', 'category').prefetch_related('tags'),
        slug=slug,
        is_published=True
    )

    # Ko'rishlar sonini oshirish
    Post.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
    post.refresh_from_db(fields=['views_count'])

    # Izohlar
    comments = post.comments.filter(is_approved=True, parent__isnull=True).select_related('user__profile').prefetch_related('replies__user__profile')

    # O'xshash maqolalar
    related_posts = Post.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'comments': comments,
        'comments_count': post.comments.filter(is_approved=True).count(),
        'related_posts': related_posts,
    }
    return render(request, 'blog/detail.html', context)


@require_POST
def web_post_comment_view(request, slug):
    """Maqolaga izoh qo'shish."""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    content = request.POST.get('content', '').strip()
    author_name = request.POST.get('author_name', '').strip()
    parent_id = request.POST.get('parent_id')

    if not content:
        messages.error(request, "Izoh matnini kiritishingiz kerak.")
        return redirect('blog_detail', slug=post.slug)

    parent_comment = None
    if parent_id:
        parent_comment = Comment.objects.filter(id=parent_id, post=post).first()

    if request.user.is_authenticated:
        Comment.objects.create(
            post=post,
            user=request.user,
            content=content,
            parent=parent_comment,
            is_approved=True
        )
    else:
        if not author_name:
            author_name = "Mehmon"
        Comment.objects.create(
            post=post,
            author_name=author_name,
            content=content,
            parent=parent_comment,
            is_approved=True
        )

    messages.success(request, "Fikringiz muvaffaqiyatli qoldirildi.")
    return redirect(f"{post.get_absolute_url()}#comments")


# ==============================================================================
# REST API VIEWS
# ==============================================================================

class BlogCategoryListAPIView(generics.ListAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.AllowAny]


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Post.objects.filter(is_published=True).select_related('author__profile', 'category').prefetch_related('tags')
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(category__slug=cat)
        tag = self.request.query_params.get('tag')
        if tag:
            qs = qs.filter(tags__slug=tag)
        q = self.request.query_params.get('search')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(content__icontains=q))
        return qs


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.filter(is_published=True).select_related('author__profile', 'category')
    serializer_class = PostDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Post.objects.filter(pk=instance.pk).update(views_count=F('views_count') + 1)
        instance.refresh_from_db(fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user, is_approved=True)
