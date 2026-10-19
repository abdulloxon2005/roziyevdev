from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import BlogCategory, Tag, Post, Comment


class BlogCategorySerializer(serializers.ModelSerializer):
    posts_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug', 'description', 'posts_count']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    display_author = serializers.CharField(read_only=True)
    avatar_url = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'user',
            'author_name',
            'display_author',
            'avatar_url',
            'content',
            'parent',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.display_name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    cover_url = serializers.CharField(read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'author_name',
            'category_name',
            'tags',
            'cover_url',
            'summary',
            'reading_time',
            'views_count',
            'comments_count',
            'published_at',
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.display_name', read_only=True)
    author_avatar = serializers.CharField(source='author.profile.avatar_url', read_only=True)
    category = BlogCategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    cover_url = serializers.CharField(read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'author_name',
            'author_avatar',
            'category',
            'tags',
            'cover_url',
            'summary',
            'content',
            'reading_time',
            'views_count',
            'comments',
            'published_at',
            'created_at',
        ]

    @extend_schema_field(CommentSerializer(many=True))
    def get_comments(self, obj):
        comments = obj.comments.filter(is_approved=True, parent__isnull=True).select_related('user__profile')
        return CommentSerializer(comments, many=True).data

