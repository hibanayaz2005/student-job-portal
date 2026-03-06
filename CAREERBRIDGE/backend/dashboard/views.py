from django.shortcuts import render, redirect
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

    # Resume Upload Analysis
    if request.method == 'POST' and request.FILES.get('resume_file'):

        uploaded_pdf = request.FILES['resume_file']

        try:

            pdf_reader = PyPDF2.PdfReader(uploaded_pdf)

            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""

            text_lower = text.lower()

            score = 40
            improvements = []
            ats_issues = []

            contact_keywords = ["gmail.com", "linkedin.com", "github.com", "phone", "+91"]
            found_contacts = [k for k in contact_keywords if k in text_lower]

            score += len(found_contacts) * 5

            if len(found_contacts) < 3:
                improvements.append("Add missing contact details (LinkedIn, GitHub, or professional email).")

            if any(x in text_lower for x in ["university", "college", "b.tech", "bachelor"]):
                score += 15
            else:
                improvements.append("Clearly state your degree and institution name.")

            tech_keywords = ["python", "django", "react", "javascript", "html", "css", "sql", "java", "git", "aws"]
            found_skills = [kw for kw in tech_keywords if kw in text_lower]

            score += len(found_skills) * 4

            if len(found_skills) < 5:
                missing = [k for k in tech_keywords if k not in found_skills][:3]
                improvements.append(
                    f"Your tech stack seems thin. Consider adding skills like: {', '.join(missing)}"
                )

            if "table" in text_lower or "\t" in text:
                ats_issues.append("Complex formatting or tables detected; many ATS cannot parse these.")

            if len(text) > 3000:
                ats_issues.append("Resume text is very long. Aim for a concise 1-page resume.")

            score = min(score, 100)

            return JsonResponse({
                'success': True,
                'score': score,
                'skills_found': found_skills,
                'improvements': improvements if improvements else ["Great job! Your resume is highly optimized."],
                'ats_issues': ats_issues if ats_issues else ["No major ATS compatibility issues found."],
                'filename': uploaded_pdf.name
            })

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    elif request.user.is_authenticated:

        user_analysis = ResumeAnalysis.objects.filter(student__user=request.user).last()

        if user_analysis:
            context['analysis'] = {
                'overall_score': getattr(user_analysis, 'overall_score', 85)
            }

    return render(request, 'dashboard/home.html', context)

    def student_portal(request):
        return render(request, 'dashboard/student-portal.html')