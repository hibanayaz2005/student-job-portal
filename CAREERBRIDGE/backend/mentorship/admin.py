from django.contrib import admin
from .models import MentorProfile, MentorSession, Message


@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mentor_type', 'company', 'rating', 'is_available', 'is_approved')
    list_filter = ('mentor_type', 'is_available', 'is_approved')
    search_fields = ('user__username', 'user__email', 'company', 'designation')


@admin.register(MentorSession)
class MentorSessionAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'student', 'topic', 'session_date', 'status')
    list_filter = ('status',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'text', 'is_read', 'created_at')
    list_filter = ('is_read',)
