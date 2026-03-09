from django.db import models
from django.conf import settings


class MentorProfile(models.Model):
    """A mentor can be a senior student, alumni, or industry professional."""
    MENTOR_TYPE_CHOICES = [
        ('senior', 'Senior Student'),
        ('alumni', 'Alumni'),
        ('professional', 'Industry Professional'),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_profile'
    )
    mentor_type = models.CharField(max_length=20, choices=MENTOR_TYPE_CHOICES, default='senior')
    expertise = models.JSONField(default=list, help_text='List of expertise areas')
    bio = models.TextField(blank=True)
    company = models.CharField(max_length=200, blank=True)
    designation = models.CharField(max_length=200, blank=True)
    years_experience = models.IntegerField(default=0)
    rating = models.FloatField(default=5.0)
    sessions_completed = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mentor: {self.user.get_full_name() or self.user.username}"


class MentorSession(models.Model):
    """Booking a mentorship session."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='sessions')
    student = models.ForeignKey(
        'accounts.StudentProfile', on_delete=models.CASCADE, related_name='mentor_sessions'
    )
    topic = models.CharField(max_length=300)
    session_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session: {self.student} → {self.mentor} ({self.status})"


class Message(models.Model):
    """Chat messages between student and mentor."""
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages'
    )
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.text[:50]}"
