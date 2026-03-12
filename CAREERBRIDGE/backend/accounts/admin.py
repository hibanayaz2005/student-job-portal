from django.contrib import admin
from .models import User, StudentProfile, EmployerProfile

<<<<<<< HEAD

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college_name', 'branch', 'year_of_study', 'is_verified', 'resume_score')
    list_filter = ('year_of_study', 'is_verified', 'aptitude_passed')
    search_fields = ('user__username', 'college_name')


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'industry', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('company_name',)
=======
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'college_name', 'year_of_study', 'is_verified')
    list_filter = ('year_of_study', 'is_verified')

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'industry', 'is_verified')
>>>>>>> 0b0f1a661d9fad69408034b791d0366a517855f9
