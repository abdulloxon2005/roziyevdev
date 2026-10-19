from django.contrib import admin
from .models import Project, ProjectLike, ProjectFile


class ProjectFileInline(admin.TabularInline):
    model = ProjectFile
    extra = 1
    fields = ('name', 'is_folder', 'parent', 'order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'language', 'project_mode', 'status', 'is_submitted', 'score', 'created_at')
    list_filter = ('language', 'project_mode', 'status', 'is_submitted', 'course')
    search_fields = ('title', 'author__email', 'tech_stack', 'tagline')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectFileInline]


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'parent', 'is_folder', 'created_at')
    list_filter = ('is_folder', 'project')
    search_fields = ('name', 'project__title')


@admin.register(ProjectLike)
class ProjectLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_at')
    search_fields = ('user__email', 'project__title')

