from django.contrib import admin
from .models import Project, ProjectMember, ProjectComment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'status', 'max_collaborators', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role', 'status', 'joined_at')
    list_filter = ('role', 'status')


@admin.register(ProjectComment)
class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'author', 'created_at')
