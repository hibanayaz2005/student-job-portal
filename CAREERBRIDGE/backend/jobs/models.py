from django.db import models


class Job(models.Model):
    # 1. Foreign key (from your first definition)
    employer = models.ForeignKey('accounts.EmployerProfile', on_delete=models.CASCADE, null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    
    # 2. All other fields (from your second definition)
    job_type = models.CharField(max_length=50, choices=[('FT', 'Full-time'), ('PT', 'Part-time')])
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200, default="To Be Announced")
    location = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.CharField(max_length=100)
    eligible_years = models.CharField(max_length=100) 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class Application(models.Model):
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, default='applied') 
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'job']