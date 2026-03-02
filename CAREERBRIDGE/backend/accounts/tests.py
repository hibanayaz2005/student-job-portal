from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountProfileTests(TestCase):
    def setUp(self):
        # create a student user
        self.student = User.objects.create_user(username='stu', password='pass', role='student')
        self.employer = User.objects.create_user(username='emp', password='pass', role='employer')
        self.client = Client()

    def test_profile_created_on_registration(self):
        self.assertTrue(hasattr(self.student, 'student_profile'))
        self.assertTrue(hasattr(self.employer, 'employer_profile'))

    def test_profile_api_get(self):
        self.client.login(username='stu', password='pass')
        resp = self.client.get('/api/auth/profile/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['username'], 'stu')
        self.assertIn('student_profile', data)
        # new fields should exist
        self.assertIn('certifications', data['student_profile'])
        self.assertIn('linkedin_url', data['student_profile'])
        self.assertIn('aptitude_passed', data['student_profile'])

    def test_profile_api_update(self):
        self.client.login(username='stu', password='pass')
        new_college = 'Test College'
        resp = self.client.put('/api/auth/profile/', {
            'student_profile': {'college_name': new_college, 'certifications': 'Cert1, Cert2', 'linkedin_url': 'http://linkedin.example', 'aptitude_passed': True}
        }, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.student.refresh_from_db()
        self.student.refresh_from_db()
        self.assertEqual(self.student.student_profile.college_name, new_college)
        self.assertEqual(self.student.student_profile.certifications, ['Cert1', 'Cert2'])
        self.assertEqual(self.student.student_profile.linkedin_url, 'http://linkedin.example')
        self.assertTrue(self.student.student_profile.aptitude_passed)

    def test_settings_page_requires_login(self):
        resp = self.client.get('/api/auth/settings/')
        self.assertEqual(resp.status_code, 302)  # redirected to login

    def test_settings_page_update(self):
        self.client.login(username='emp', password='pass')
        # API path should still work
        resp = self.client.post('/api/auth/settings/', {
            'company_name': 'NewCo',
            'industry': 'Tech',
        })
        self.assertEqual(resp.status_code, 302)
        self.employer.refresh_from_db()
        self.assertEqual(self.employer.employer_profile.company_name, 'NewCo')

    def test_logout_route(self):
        self.client.login(username='stu', password='pass')
        # hitting the API logout path also works
        resp = self.client.get('/api/auth/logout/')
        # should redirect to login
        self.assertEqual(resp.status_code, 302)
        # subsequent request should show not authenticated
        resp2 = self.client.get('/api/auth/profile/')
        # once logged out, access is forbidden
        self.assertIn(resp2.status_code, (401,403))

    def test_dashboard_links(self):
        # unauthenticated or authenticated should see settings link
        self.client.login(username='stu', password='pass')
        from django.test import Client
        c = Client()
        c.login(username='stu', password='pass')
        resp = c.get('/')
        self.assertContains(resp, 'href="/accounts/settings/"')
        self.assertContains(resp, 'href="/accounts/logout/"')
        # profile link should now be an anchor pointing at settings
        self.assertContains(resp, '<a class="dash-nav-item" href="/accounts/settings/">')

    def test_login_api_validation(self):
        # missing fields should return 400
        resp = self.client.post('/api/auth/login/', {}, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('username', resp.json().get('error',''))

    def test_session_login_page(self):
        # GET should display login form and not show API hint
        resp = self.client.get('/accounts/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, '/api/auth/login/')
        # Google sign-in link present
        self.assertContains(resp, 'Sign in with Google')
        # POST wrong credentials shows error
        resp2 = self.client.post('/accounts/login/', {'username':'no','password':'no'})
        self.assertContains(resp2, 'Invalid credentials')
        # create a user and login successfully
        u = User.objects.create_user(username='bob', password='pw', role='student')
        resp3 = self.client.post('/accounts/login/', {'username':'bob','password':'pw'})
        self.assertEqual(resp3.status_code, 302)
        # after login, homepage should show settings link
        resp4 = self.client.get('/')
        self.assertContains(resp4, '/accounts/settings/')
