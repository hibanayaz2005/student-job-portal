from django.db import models

from django.conf import settings


from django.db import models
from django.conf import settings

class Job(models.Model):
    JOB_TYPES = [
        ('internship', 'Internship'),
        ('fulltime', 'Full Time'),
        ('parttime', 'Part Time'),
        ('freelance', 'Freelance'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    description = models.TextField()
    salary = models.CharField(max_length=100)
    deadline = models.DateField()

    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=300)
    provider = models.CharField(max_length=50)  # YouTube, NPTEL, etc.


class Course(models.Model):
    title = models.CharField(max_length=300)
    provider = models.CharField(max_length=50) # YouTube, NPTEL, etc.

    provider_url = models.URLField()
    category = models.CharField(max_length=100)
    target_years = models.JSONField(default=list)
    is_free = models.BooleanField(default=True)

    description = models.TextField(blank=True)
    duration = models.CharField(max_length=50, blank=True)
    icon = models.CharField(max_length=10, default='📚')

    def __str__(self):
        return self.title



class CourseProgress(models.Model):
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    status = models.CharField(max_length=15, default='not_started')
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student} - {self.course.title} ({self.status})"


class SkillTest(models.Model):
    """Skill assessment test linked to a course."""
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='skill_test')
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    passing_score = models.IntegerField(default=70)
    time_limit_minutes = models.IntegerField(default=30)
    questions = models.JSONField(
        default=list,
        help_text='List of {question, options: [], correct_index, explanation}'
    )

    def __str__(self):
        return self.title


class TestAttempt(models.Model):
    """Record of a student taking a skill test."""
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    test = models.ForeignKey(SkillTest, on_delete=models.CASCADE)
    answers = models.JSONField(default=list)
    score = models.IntegerField(default=0)
    passed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.test.title} ({self.score}%)"


class Certificate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(SkillTest, on_delete=models.CASCADE)
    certificate_id = models.CharField(max_length=100)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to="certificates/", null=True, blank=True)
    
    def __str__(self):
        return f"Certificate: {self.student} - {self.test.title}"

    status = models.CharField(max_length=15, default='not_started')

