import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')
django.setup()

from django.contrib.auth import get_user_model
from mentorship.models import MentorProfile

User = get_user_model()

def seed_mentors():
    mentors_data = [
        {
            'username': 'ravi_google',
            'email': 'ravi@google.com',
            'first_name': 'Ravi',
            'last_name': 'Patil',
            'type': 'professional',
            'expertise': ['System Design', 'DSA', 'Career Strategy'],
            'company': 'Google',
            'designation': 'Senior Engineer',
            'bio': '12+ years in tech. Ex-Amazon, now at Google. Passionate about mentoring students.'
        },
        {
            'username': 'sneha_ms',
            'email': 'sneha@microsoft.com',
            'first_name': 'Sneha',
            'last_name': 'Kumar',
            'type': 'alumni',
            'expertise': ['React', 'Full Stack', 'Interview Prep'],
            'company': 'Microsoft',
            'designation': 'SDE-2',
            'bio': 'IIT Madras alumna. Loves helping juniors crack product company interviews.'
        },
        {
            'username': 'arjun_iit',
            'email': 'arjun@iitd.ac.in',
            'first_name': 'Arjun',
            'last_name': 'Jha',
            'type': 'senior',
            'expertise': ['CP', 'DSA', 'Placement Prep'],
            'company': 'IIT Delhi',
            'designation': 'Final Year Student',
            'bio': '300+ problems on LeetCode. Placed at Goldman Sachs. Ready to help 3rd years.'
        }
    ]

    for m in mentors_data:
        user, created = User.objects.get_or_create(
            username=m['username'],
            defaults={
                'email': m['email'],
                'first_name': m['first_name'],
                'last_name': m['last_name'],
                'role': 'mentor'
            }
        )
        if created:
            user.set_password('mentor123')
            user.save()
            print(f"Created user {user.username}")

        profile, p_created = MentorProfile.objects.get_or_create(
            user=user,
            defaults={
                'mentor_type': m['type'],
                'expertise': m['expertise'],
                'bio': m['bio'],
                'company': m['company'],
                'designation': m['designation'],
                'years_experience': random.randint(1, 15),
                'is_approved': True,
                'is_available': True
            }
        )
        if p_created:
            print(f"Created mentor profile for {user.username}")
        else:
            # Update existing if needed
            profile.is_approved = True
            profile.is_available = True
            profile.save()
            print(f"Updated mentor profile for {user.username}")

if __name__ == '__main__':
    seed_mentors()
