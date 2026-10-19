from django.contrib import admin
from .models import Contest, ContestProblem, ContestParticipant, ContestSubmission


class ContestProblemInline(admin.TabularInline):
    model = ContestProblem
    extra = 1
    fields = ('order', 'title', 'difficulty', 'points')


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_time', 'end_time', 'coin_prize_pool', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ContestProblemInline]


@admin.register(ContestProblem)
class ContestProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'contest', 'order', 'difficulty', 'points')
    list_filter = ('contest', 'difficulty')
    search_fields = ('title', 'description')


@admin.register(ContestParticipant)
class ContestParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'contest', 'total_score', 'rank', 'created_at')
    list_filter = ('contest',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')


@admin.register(ContestSubmission)
class ContestSubmissionAdmin(admin.ModelAdmin):
    list_display = ('participant', 'problem', 'score', 'status', 'created_at')
    list_filter = ('status', 'problem__contest')
    search_fields = ('participant__user__email', 'problem__title')
