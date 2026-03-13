from django.contrib import admin

from .models import Job, Application


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'location', 'salary', 'is_active', 'created_at')
    list_filter = ('job_type', 'is_active')
    search_fields = ('title', 'company', 'description')


from .models import Job, Application # Import the blueprint from models.py

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'eligible_years', 'is_active')
    list_filter = ('is_active', 'eligible_years')
    search_fields = ('title', 'company')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'status', 'applied_at')


    list_filter = ('status',)

    list_editable = ('status',)

