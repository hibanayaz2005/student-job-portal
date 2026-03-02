from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=300)
    provider = models.CharField(max_length=50) # YouTube, NPTEL, etc.
    provider_url = models.URLField()
    category = models.CharField(max_length=100)
    target_years = models.JSONField(default=list)
    is_free = models.BooleanField(default=True)

class CourseProgress(models.Model):
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, default='not_started')