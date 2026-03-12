from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta

from django.views.decorators.csrf import ensure_csrf_cookie
import json
import random
import PyPDF2

from jobs.models import Job, Application
from courses.models import Course
from resume.models import ResumeAnalysis
from .models import OTPVerification

import requests

# Temporary OTP storage
OTP_STORE = {}

def create_notification(user, title, message):
    from .models import Notification
    return Notification.objects.create(user=user, title=title, message=message)

def get_notifications(request):
    if not request.user.is_authenticated:
        return JsonResponse({"notifications": []})
    from .models import Notification
    notes = Notification.objects.filter(user=request.user)[:10]
    data = [{
        "id": n.id,
        "title": n.title,
        "message": n.message,
        "is_read": n.is_read,
        "created_at": n.created_at.strftime("%Y-%m-%d %H:%M")
    } for n in notes]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({"notifications": data, "unread_count": unread_count})

@require_POST
def mark_notification_read(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False}, status=401)
    from .models import Notification
    data = json.loads(request.body)
    note_id = data.get("id")
    if note_id:
        Notification.objects.filter(id=note_id, user=request.user).update(is_read=True)
    else:
        Notification.objects.filter(user=request.user).update(is_read=True)
    return JsonResponse({"success": True})

@require_POST
def send_aadhaar_otp(request):

    data = json.loads(request.body)
    phone = data.get("phone")

    if not phone:
        return JsonResponse({"error": "Phone required"}, status=400)

    otp = random.randint(100000, 999999)

    # save OTP in database
    OTPVerification.objects.create(
        phone=phone,
        otp=otp
    )

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "route": "q",
        "message": f"Your CareerBridge OTP is {otp}",
        "language": "english",
        "numbers": phone
    }

    headers = {
        "authorization": settings.FAST2SMS_API_KEY,
        "Content-Type": "application/json"
    }

    requests.post(url, json=payload, headers=headers)

    return JsonResponse({"message": "OTP sent"})

@require_POST
def verify_aadhaar_otp(request):

    data = json.loads(request.body)

    phone = data.get("phone")
    otp = data.get("otp")

    if not phone or not otp:
        return JsonResponse({"verified": False})

    try:

        record = OTPVerification.objects.filter(phone=phone).latest("created_at")

        # check expiry (5 minutes)
        if timezone.now() - record.created_at > timedelta(minutes=5):
            return JsonResponse({
                "verified": False,
                "error": "OTP expired"
            })

        if record.otp == int(otp):

            record.delete()

            return JsonResponse({
                "verified": True
            })

        return JsonResponse({"verified": False})

    except OTPVerification.DoesNotExist:

        return JsonResponse({"verified": False})


@ensure_csrf_cookie
def student_portal(request):
    return render(request, 'dashboard/student-portal.html')


def home(request):

    User = get_user_model()

    now = timezone.now()

    upcoming_deadlines = Job.objects.filter(
        deadline__gte=now,
        deadline__lte=now + timedelta(days=2)
    )

    users_count = User.objects.count()
    jobs_count = Job.objects.count()
    courses_count = Course.objects.count()
    applications_count = Application.objects.count()

    role_qs = User.objects.values('role').annotate(count=Count('id'))
    role_labels = [r['role'].capitalize() for r in role_qs if r.get('role')]
    role_values = [r['count'] for r in role_qs if r.get('role')]

    jobs_qs = Job.objects.values('job_type').annotate(count=Count('id'))
    job_labels = [j['job_type'].capitalize() for j in jobs_qs if j.get('job_type')]
    job_values = [j['count'] for j in jobs_qs if j.get('job_type')]

    recent_qs = Application.objects.select_related('job__employer').order_by('-applied_at')[:5]

    recent_apps = [
        {
            'company': app.job.employer.company_name if app.job and hasattr(app.job, 'employer') else 'Company',
            'role': app.job.title if app.job else 'Role',
            'status': app.status,
        }
        for app in recent_qs
    ]

    context = {
        'users_count': users_count,
        'jobs_count': jobs_count,
        'courses_count': courses_count,
        'applications_count': applications_count,
        'role_labels': json.dumps(role_labels),
        'role_values': json.dumps(role_values),
        'job_labels': json.dumps(job_labels),
        'job_values': json.dumps(job_values),
        'recent_apps': recent_apps,
        'user': request.user,
        'upcoming_deadlines': upcoming_deadlines,
    }

    return render(request, 'dashboard/home.html', context)