from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
import json
import random
import PyPDF2

from jobs.models import Job, Application
from courses.models import Course
from resume.models import ResumeAnalysis

import requests

# Temporary OTP storage
OTP_STORE = {}


def send_aadhaar_otp(request):

    if request.method == "POST":

        data = json.loads(request.body)
        phone = data.get("phone")

        otp = random.randint(100000, 999999)

        OTP_STORE[phone] = otp

        url = "https://www.fast2sms.com/dev/bulkV2"

        payload = {
            "route": "q",
            "message": f"Your CareerBridge OTP is {otp}",
            "language": "english",
            "numbers": phone
        }

        headers = {
            "authorization": "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",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.text)   # IMPORTANT for debugging

        return JsonResponse({"message": "OTP request sent"})


def verify_aadhaar_otp(request):

    if request.method == "POST":

        try:

            data = json.loads(request.body)

            phone = data.get("phone")
            otp = data.get("otp")

            if not phone or not otp:
                return JsonResponse({"verified": False})

            if OTP_STORE.get(phone) == int(otp):

                # remove OTP after success
                del OTP_STORE[phone]

                return JsonResponse({
                    "verified": True
                })

            return JsonResponse({
                "verified": False
            })

        except:
            return JsonResponse({"verified": False})

    return JsonResponse({"verified": False})


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