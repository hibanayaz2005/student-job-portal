from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.db import models



class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username

class StudentProfile(models.Model):
    YEAR_CHOICES = [
        (1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'),
        (4, 'Final Year'), (5, 'Post Graduate'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    college_name = models.CharField(max_length=200)
    branch = models.CharField(max_length=100)
    year_of_study = models.IntegerField(choices=YEAR_CHOICES)
    graduation_year = models.IntegerField()
    skills = models.JSONField(default=list)
    certifications = models.JSONField(default=list, blank=True)
    linkedin_url = models.URLField(blank=True)
    aptitude_passed = models.BooleanField(default=False)
    resume_score = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.college_name}"

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            StudentProfile.objects.create(user=instance, year_of_study=1, graduation_year=2026, college_name='', branch='')
        elif instance.role == 'employer':
            EmployerProfile.objects.create(user=instance, company_name='', industry='')