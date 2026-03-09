from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=300)
    provider = models.CharField(max_length=50)  # YouTube, NPTEL, etc.
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
    """Certificate issued after passing a skill test."""
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE)
    test = models.ForeignKey(SkillTest, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Certificate: {self.student} - {self.test.title}"