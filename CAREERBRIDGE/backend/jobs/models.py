from django.db import models

class Job(models.Model):
    employer = models.ForeignKey('accounts.EmployerProfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=[('internship', 'Internship'), ('full_time', 'Full-time')])
    eligible_years = models.JSONField(default=list)  # e.g., [3, 4]
    location = models.CharField(max_length=200)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Application(models.Model):
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'job']