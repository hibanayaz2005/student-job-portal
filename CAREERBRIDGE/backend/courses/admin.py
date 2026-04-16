from django.contrib import admin
from .models import Course, CourseProgress, SkillTest, TestAttempt, Certificate

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'target_program', 'category', 'is_free')
    list_filter = ('target_program', 'category', 'is_free')

@admin.register(SkillTest)
class SkillTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'passing_score', 'time_limit_minutes')
    
@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'completed_at')
    
@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'passed', 'attempted_at')
    
@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'certificate_id', 'status', 'issued_at')
