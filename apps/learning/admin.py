from django.contrib import admin
from .models import Enrollment, LessonProgress, Assignment, AssignmentSubmission, CoinTransaction


class LessonProgressInline(admin.TabularInline):
    model = LessonProgress
    extra = 0
    readonly_fields = ('lesson', 'created_at')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'progress_percent', 'is_completed', 'completed_at', 'updated_at')
    list_filter = ('course', 'completed_at')
    search_fields = ('user__email', 'user__username', 'course__title')
    inlines = [LessonProgressInline]


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'created_at')
    list_filter = ('enrollment__course',)
    search_fields = ('enrollment__user__email', 'lesson__title')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'coin_reward', 'passing_score', 'max_score', 'is_active', 'created_at')
    list_filter = ('is_active', 'lesson__module__course')
    search_fields = ('title', 'description', 'lesson__title')
    list_editable = ('coin_reward', 'passing_score', 'is_active')


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'score', 'coins_awarded', 'reviewed_by', 'reviewed_at', 'created_at')
    list_filter = ('status', 'assignment__lesson__module__course', 'created_at')
    search_fields = ('student__email', 'student__first_name', 'student__last_name', 'assignment__title')
    readonly_fields = ('coins_awarded', 'reviewed_at', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('student__email', 'description')
    ordering = ('-created_at',)
