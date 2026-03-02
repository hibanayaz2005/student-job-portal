from django.contrib import admin
from .models import User, StudentProfile, EmployerProfile

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