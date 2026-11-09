from django.contrib import admin

from .models import (
    AssessmentAttempt,
    AssessmentItem,
    CodeDraft,
    LessonBlock,
    ModuleAssessment,
    Task,
    TaskAttempt,
    TaskOption,
    TaskProgress,
    TaskTest,
)


class TaskOptionInline(admin.TabularInline):
    model = TaskOption
    extra = 0
    fields = ('order', 'text', 'is_correct', 'feedback')


class TaskTestInline(admin.StackedInline):
    model = TaskTest
    extra = 0
    fields = (('order', 'check_type', 'ignore_case', 'is_hidden'), 'description', 'stdin', 'expected', 'failure_message')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'logical_name', 'section', 'kind', 'difficulty', 'points', 'order', 'is_published')
    list_filter = ('module__course', 'module', 'section', 'kind', 'difficulty', 'is_published')
    search_fields = ('title', 'prompt', 'lesson__title')
    list_editable = ('order', 'is_published')
    autocomplete_fields = ('lesson',)
    inlines = [TaskOptionInline, TaskTestInline]
    fieldsets = (
        (None, {'fields': ('module', 'lesson', ('section', 'kind', 'difficulty'), ('order', 'points', 'is_published'), 'title', 'prompt')}),
        ("Kod va javob", {'fields': ('code_snippet', 'starter_code', 'expected_output_example', 'correct_answer')}),
        ("Yordam va yechim", {'fields': ('hint', 'partial_solution', 'full_solution', 'solution_unlock_attempts', 'explanation')}),
    )


class LessonBlockInline(admin.StackedInline):
    model = LessonBlock
    extra = 0
    fk_name = 'lesson'
    fields = (('order', 'block_type', 'callout_style'), 'title', 'body', 'code', 'is_runnable', 'image', 'video_url', 'task')


@admin.register(LessonBlock)
class LessonBlockAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'order', 'block_type', 'title')
    list_filter = ('block_type', 'lesson__module__course')
    search_fields = ('title', 'body', 'lesson__title')


class AssessmentItemInline(admin.TabularInline):
    model = AssessmentItem
    extra = 0
    autocomplete_fields = ('task',)


@admin.register(ModuleAssessment)
class ModuleAssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'pass_percent', 'max_attempts', 'is_published')
    list_filter = ('module__course', 'is_published')
    inlines = [AssessmentItemInline]


@admin.register(TaskProgress)
class TaskProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'status', 'attempts_count', 'best_score', 'solved_at', 'solution_viewed')
    list_filter = ('status', 'task__module__course')
    search_fields = ('user__email', 'task__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TaskAttempt)
class TaskAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'context', 'attempt_number', 'is_correct', 'score', 'max_score', 'created_at')
    list_filter = ('context', 'is_correct', 'task__module__course')
    search_fields = ('user__email', 'task__title')
    readonly_fields = [f.name for f in TaskAttempt._meta.fields]


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'assessment', 'attempt_number', 'percent', 'passed', 'created_at')
    list_filter = ('passed', 'assessment')
    search_fields = ('user__email',)
    readonly_fields = [f.name for f in AssessmentAttempt._meta.fields]


@admin.register(CodeDraft)
class CodeDraftAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'key', 'updated_at')
    search_fields = ('user__email', 'key')
