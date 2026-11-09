from django.contrib import admin
from .models import Category, Course, CourseModule, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'lesson_type', 'duration_minutes', 'is_preview', 'is_published', 'order')


class CourseModuleInline(admin.StackedInline):
    model = CourseModule
    extra = 1
    fields = ('title', 'description', 'order', 'is_published')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'level', 'price', 'is_free', 'is_published', 'is_featured', 'is_archived')
    list_filter = ('category', 'level', 'is_free', 'is_published', 'is_featured', 'is_archived')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CourseModuleInline]


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_published')
    list_filter = ('course', 'is_published')
    list_editable = ('order', 'is_published')
    search_fields = ('title', 'course__title')
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'lesson_type', 'duration_minutes', 'is_preview', 'is_published', 'order')
    list_filter = ('is_preview', 'is_published', 'lesson_type', 'module__course')
    search_fields = ('title', 'module__title')
    list_editable = ('order', 'is_published')

    def get_inlines(self, request, obj):
        from apps.interactive.admin import LessonBlockInline
        return [LessonBlockInline]
