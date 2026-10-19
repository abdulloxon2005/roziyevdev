from django.contrib import admin
from .models import BlogCategory, Tag, Post, Comment


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'reading_time', 'views_count', 'is_published', 'published_at')
    list_filter = ('is_published', 'category', 'tags', 'published_at')
    search_fields = ('title', 'summary', 'content', 'author__email')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('reading_time', 'views_count', 'created_at', 'updated_at')
    ordering = ('-published_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('display_author', 'post', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('content', 'author_name', 'user__email', 'post__title')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Tanlangan izohlarni tasdiqlash"
