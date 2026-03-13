from django.contrib import admin

from .models import Course, CourseProgress, SkillTest, TestAttempt, Certificate


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider', 'category', 'is_free')
    list_filter = ('provider', 'is_free', 'category')
    search_fields = ('title',)
    ordering = ('title',)

@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status')
    list_filter = ('status',)


@admin.register(SkillTest)
class SkillTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'passing_score', 'time_limit_minutes')


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'score', 'passed', 'attempted_at')
    list_filter = ('passed',)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'test', 'certificate_id', 'issued_at')
=======

# Register your models here.
>>>>>>> 0b0f1a661d9fad69408034b791d0366a517855f9
