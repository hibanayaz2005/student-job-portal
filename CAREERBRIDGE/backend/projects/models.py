from django.db import models
from django.conf import settings


class Project(models.Model):
    """Student collaborative projects."""
    STATUS_CHOICES = [
        ('open', 'Open for Collaboration'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=300)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    max_collaborators = models.IntegerField(default=4)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_projects'
    )
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def current_members(self):
        return self.members.filter(status='accepted').count()


class ProjectMember(models.Model):
    """Links students to projects."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    ROLE_CHOICES = [
        ('lead', 'Team Lead'),
        ('member', 'Member'),
        ('mentor', 'Mentor'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['project', 'user']

    def __str__(self):
        return f"{self.user.username} → {self.project.title} ({self.role})"


class ProjectComment(models.Model):
    """Feedback from mentors or peers on projects."""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.project.title} by {self.author.username}"
