from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Count
import json

from jobs.models import Job, Application
from courses.models import Course
from django.utils import timezone
from datetime import timedelta
from resume.models import ResumeAnalysis


import random  # Make sure this is here!

<div class="score-circle" style="background: conic-gradient(var(--accent) 0deg, var(--accent) {{ analysis.score_deg }}deg, var(--border) {{ analysis.score_deg }}deg);">
# Inside your home view:
now = timezone.now()
upcoming_deadlines = Job.objects.filter(
    deadline__gte=now, 
    deadline__lte=now + timedelta(days=2) # Alert for deadlines in next 48 hours
)


 # Assuming your resume model name

def home(request):
    has_resume = False
    if request.user.is_authenticated:
        has_resume = Resume.objects.filter(user=request.user).exists()
    
    return render(request, 'dashboard/home.html', {
        'has_resume': has_resume,
        # ... other context ...
    })

def home(request):
    User = get_user_model()

    users_count = User.objects.count()
    jobs_count = Job.objects.count()
    courses_count = Course.objects.count()
    applications_count = Application.objects.count()

    # Role distribution for chart
    role_qs = User.objects.values('role').annotate(count=Count('id'))
    role_labels = [r['role'].capitalize() for r in role_qs]
    role_values = [r['count'] for r in role_qs]

    # Jobs by type for chart
    jobs_qs = Job.objects.values('job_type').annotate(count=Count('id'))
    job_labels = [j['job_type'].capitalize() for j in jobs_qs]
    job_values = [j['count'] for j in jobs_qs]

    # Recent applications (latest 5)
    recent_qs = Application.objects.select_related('job__employer').order_by('-applied_at')[:5]
    recent_apps = [
        {
            'company': app.job.employer.company_name if app.job and app.job.employer else 'Company',
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
