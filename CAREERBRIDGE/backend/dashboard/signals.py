from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from jobs.models import Job, Application
from mentorship.models import MentorSession
from courses.models import TestAttempt
from .models import Notification
from accounts.models import StudentProfile

User = get_user_model()

def send_ws_notification(user_id, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_notifications_{user_id}",
        {
            "type": "send_notification",
            "data": data
        }
    )

def broadcast_platform_update(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "platform_analytics",
        {
            "type": "platform_update",
            "data": data
        }
    )

@receiver(post_save, sender=TestAttempt)
def test_pass_analytics(sender, instance, created, **kwargs):
    if created and instance.passed:
        broadcast_platform_update({
            "type": "test_pass",
            "user": instance.student.user.first_name or instance.student.user.username,
            "course": instance.test.course.title,
            "score": instance.score
        })

@receiver(post_save, sender=Application)
def application_analytics(sender, instance, created, **kwargs):
    if created:
        broadcast_platform_update({
            "type": "new_app",
            "user": instance.student.user.first_name or instance.student.user.username,
            "job": instance.job.title,
            "company": instance.job.employer.company_name if hasattr(instance.job, 'employer') else "Company"
        })

@receiver(post_save, sender=MentorSession)
def mentor_session_notification(sender, instance, created, **kwargs):
    if not created and instance.status == 'confirmed':
        # When mentor accepts tutoring request
        notif = Notification.objects.create(
            user=instance.student.user,
            title="Tutoring Request Accepted! ✅",
            message=f"Mentor {instance.mentor.user.get_full_name()} has accepted your request for '{instance.topic}'."
        )
        send_ws_notification(instance.student.user.id, {
            "title": notif.title,
            "message": notif.message,
            "id": notif.id,
            "type": "mentor_accept"
        })

@receiver(post_save, sender=Job)
def new_job_notification(sender, instance, created, **kwargs):
    if created:
        # Match students by skill
        # For simplicity, we find students who have any of the keywords in their skills list
        # In a real app, this would be a more complex query
        students = StudentProfile.objects.all()
        for profile in students:
            # Check if any skill in job description matches profile skills
            matches = [s for s in profile.skills if s.lower() in instance.description.lower() or s.lower() in instance.title.lower()]
            if matches:
                notif = Notification.objects.create(
                    user=profile.user,
                    title="New Matching Job Found! 💼",
                    message=f"A new job '{instance.title}' at {instance.location} matches your skills: {', '.join(matches[:2])}."
                )
                send_ws_notification(profile.user.id, {
                    "title": notif.title,
                    "message": notif.message,
                    "id": notif.id,
                    "type": "new_job",
                    "link": f"/jobs/{instance.id}/"
                })

# Profile view notification will be triggered manually from a view
def notify_profile_view(viewed_user, viewer_name):
    notif = Notification.objects.create(
        user=viewed_user,
        title="Profile Viewed! 👀",
        message=f"An employer from {viewer_name} recently viewed your profile."
    )
    send_ws_notification(viewed_user.id, {
        "title": notif.title,
        "message": notif.message,
        "id": notif.id,
        "type": "profile_view"
    })
