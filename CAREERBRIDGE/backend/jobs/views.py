from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Job
from .serializers import JobSerializer
from .serializers import ApplicationSerializer
from .models import Application
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class JobListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # optional filter by year
        year = request.query_params.get('year')
        qs = Job.objects.all().order_by('-created_at')
        if year:
            try:
                y = int(year)
                qs = qs.filter(eligible_years__contains=[y])
            except Exception:
                pass
        if not qs.exists():
            sample = [
                {
                    'id': 0,
                    'employer': None,
                    'title': 'Frontend Developer Intern',
                    'description': 'React, JavaScript, CSS. Work on real products used by millions.',
                    'job_type': 'internship',
                    'eligible_years': [3,4],
                    'location': 'Chennai',
                    'deadline': '2026-12-31',
                    'created_at': None,
                },
                {
                    'id': 1,
                    'employer': None,
                    'title': 'Data Science Research Intern',
                    'description': 'Python, ML, Data Analysis. Stipend + LOR.',
                    'job_type': 'internship',
                    'eligible_years': [2,3,4],
                    'location': 'IIT Madras Research Park',
                    'deadline': '2026-11-30',
                    'created_at': None,
                }
            ]
            return Response(sample)

        serializer = JobSerializer(qs, many=True)
        return Response(serializer.data)


class JobCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # only employers may post
        user = request.user
        if not hasattr(user, 'employerprofile'):
            return Response({'detail': 'Only employers may post jobs'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['employer'] = user.employerprofile.id
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            job = serializer.save()
            return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        student = getattr(user, 'student_profile', None)
        if not student:
            return Response({'detail': 'Only students can apply'}, status=status.HTTP_403_FORBIDDEN)

        # ensure student has passed aptitude test
        if not getattr(student, 'aptitude_passed', False):
            return Response({'detail': 'Must complete aptitude test before applying'}, status=status.HTTP_403_FORBIDDEN)

        job_id = request.data.get('job_id')
        if not job_id:
            return Response({'detail': 'job_id required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({'detail': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

        # prevent duplicate
        if Application.objects.filter(student=student, job=job).exists():
            return Response({'detail': 'Already applied'}, status=status.HTTP_400_BAD_REQUEST)

        app = Application.objects.create(student=student, job=job)
        return Response({'status': 'applied', 'application_id': app.id}, status=status.HTTP_201_CREATED)
from django.shortcuts import render

# Create your views here.
