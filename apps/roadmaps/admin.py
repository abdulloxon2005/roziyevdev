from django.contrib import admin
from .models import RoadmapTrack, RoadmapStage, RoadmapNode, UserRoadmapProgress


class RoadmapNodeInline(admin.TabularInline):
    model = RoadmapNode
    extra = 1
    fields = ('order', 'title', 'importance', 'linked_course', 'linked_lesson')


class RoadmapStageInline(admin.StackedInline):
    model = RoadmapStage
    extra = 1
    fields = ('order', 'title', 'description')


@admin.register(RoadmapTrack)
class RoadmapTrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'accent_color', 'estimated_months', 'order', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RoadmapStageInline]


@admin.register(RoadmapStage)
class RoadmapStageAdmin(admin.ModelAdmin):
    list_display = ('title', 'track', 'order')
    list_filter = ('track',)
    inlines = [RoadmapNodeInline]


@admin.register(RoadmapNode)
class RoadmapNodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'stage', 'order', 'importance', 'linked_course')
    list_filter = ('stage__track', 'importance')
    search_fields = ('title', 'summary')


@admin.register(UserRoadmapProgress)
class UserRoadmapProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'node', 'status', 'completed_at')
    list_filter = ('status', 'node__stage__track')
    search_fields = ('user__email', 'node__title')
