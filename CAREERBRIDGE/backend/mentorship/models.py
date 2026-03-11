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
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Session pricing per hour")
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mentor: {self.user.get_full_name() or self.user.username}"


class MentorAvailability(models.Model):
    """Availability schedule for mentors to open time slots."""
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=[(i, str(i)) for i in range(7)], help_text="0=Monday, 6=Sunday")
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mentor} - Day {self.day_of_week} ({self.start_time}-{self.end_time})"

class MentorSession(models.Model):
    """Booking a mentorship session."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    SESSION_TYPES = [
        ('text', 'Text Chat'),
        ('video', 'Video Call'),
        ('audio', 'Audio Call'),
    ]
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='sessions')
    student = models.ForeignKey(
        'accounts.StudentProfile', on_delete=models.CASCADE, related_name='mentor_sessions'
    )
    topic = models.CharField(max_length=300)
    session_type = models.CharField(max_length=10, choices=SESSION_TYPES, default='video')
    session_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICES, default='pending')
    meeting_link = models.URLField(blank=True, null=True, help_text="WebRTC / Agora / Video meeting link")
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
