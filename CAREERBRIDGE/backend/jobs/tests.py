from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Job, Application

User = get_user_model()


class JobApplicationTests(TestCase):
    def setUp(self):
        # create employer and student
        self.emp = User.objects.create_user(username='emp', password='pass', role='employer')
        self.stu = User.objects.create_user(username='stu', password='pass', role='student')
        # ensure profile created
        self.stu.student_profile.college_name = 'Test'
        self.stu.student_profile.save()
        self.client = Client()
        # create a job
        self.job = Job.objects.create(
            employer=self.emp.employer_profile,
            title='Test Job',
            description='Desc',
            job_type='internship',
            eligible_years=[1,2,3],
            location='Remote',
            deadline='2026-12-31'
        )

    def test_cannot_apply_without_aptitude(self):
        self.client.login(username='stu', password='pass')
        resp = self.client.post('/api/jobs/apply/', {'job_id': self.job.id}, content_type='application/json')
        self.assertEqual(resp.status_code, 403)
        self.assertIn('aptitude', resp.json().get('detail','').lower())

    def test_apply_after_aptitude(self):
        self.stu.student_profile.aptitude_passed = True
        self.stu.student_profile.save()
        self.client.login(username='stu', password='pass')
        resp = self.client.post('/api/jobs/apply/', {'job_id': self.job.id}, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Application.objects.filter(student=self.stu.student_profile, job=self.job).exists())

    def test_duplicate_application(self):
        self.stu.student_profile.aptitude_passed = True
        self.stu.student_profile.save()
        self.client.login(username='stu', password='pass')
        self.client.post('/api/jobs/apply/', {'job_id': self.job.id}, content_type='application/json')
        resp2 = self.client.post('/api/jobs/apply/', {'job_id': self.job.id}, content_type='application/json')
        self.assertEqual(resp2.status_code, 400)
