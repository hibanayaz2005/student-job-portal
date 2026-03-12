#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')
django.setup()

from django.contrib.auth import get_user_model
from mentorship.models import MentorProfile, MentorAvailability
from datetime import time

User = get_user_model()

def create_sample_mentors():
    # Create sample users for mentors
    mentors_data = [
        {
            'username': 'raj_patel',
            'email': 'raj.patel@example.com',
            'first_name': 'Raj',
            'last_name': 'Patel',
            'mentor_type': 'professional',
            'expertise': ['Web Development', 'React', 'Node.js', 'Career Guidance'],
            'bio': 'Senior Software Engineer at Google with 8+ years of experience in web development and mentoring.',
            'company': 'Google',
            'designation': 'Senior Software Engineer',
            'years_experience': 8,
            'hourly_rate': 1500.00
        },
        {
            'username': 'priya_sharma',
            'email': 'priya.sharma@example.com',
            'first_name': 'Priya',
            'last_name': 'Sharma',
            'mentor_type': 'alumni',
            'expertise': ['Data Science', 'Machine Learning', 'Python', 'Interview Prep'],
            'bio': 'Data Science graduate from IIT Bombay, now working at Microsoft. Love helping students with career transitions.',
            'company': 'Microsoft',
            'designation': 'Data Scientist',
            'years_experience': 5,
            'hourly_rate': 1200.00
        },
        {
            'username': 'amit_kumar',
            'email': 'amit.kumar@example.com',
            'first_name': 'Amit',
            'last_name': 'Kumar',
            'mentor_type': 'senior',
            'expertise': ['Android Development', 'Kotlin', 'Java', 'Mobile Apps'],
            'bio': 'Final year CSE student with internship experience at Flipkart. Passionate about mobile development.',
            'company': 'N/A',
            'designation': 'Student Developer',
            'years_experience': 2,
            'hourly_rate': 500.00
        },
        {
            'username': 'sneha_reddy',
            'email': 'sneha.reddy@example.com',
            'first_name': 'Sneha',
            'last_name': 'Reddy',
            'mentor_type': 'professional',
            'expertise': ['UI/UX Design', 'Figma', 'Product Design', 'Portfolio Review'],
            'bio': 'Product Designer at Adobe with expertise in user experience and design systems.',
            'company': 'Adobe',
            'designation': 'Senior Product Designer',
            'years_experience': 6,
            'hourly_rate': 1000.00
        }
    ]
    
    for mentor_data in mentors_data:
        # Create user if doesn't exist
        user, created = User.objects.get_or_create(
            username=mentor_data['username'],
            defaults={
                'email': mentor_data['email'],
                'first_name': mentor_data['first_name'],
                'last_name': mentor_data['last_name'],
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            print(f"Created user: {user.username}")
        
        # Create mentor profile
        mentor_profile, created = MentorProfile.objects.get_or_create(
            user=user,
            defaults={
                'mentor_type': mentor_data['mentor_type'],
                'expertise': mentor_data['expertise'],
                'bio': mentor_data['bio'],
                'company': mentor_data['company'],
                'designation': mentor_data['designation'],
                'years_experience': mentor_data['years_experience'],
                'hourly_rate': mentor_data['hourly_rate'],
                'is_available': True,
                'is_approved': True
            }
        )
        
        if created:
            print(f"Created mentor profile: {mentor_profile}")
            
            # Create sample availability for each mentor
            sample_availabilities = [
                {'day_of_week': 0, 'start_time': time(18, 0), 'end_time': time(20, 0)},  # Monday 6-8 PM
                {'day_of_week': 1, 'start_time': time(19, 0), 'end_time': time(21, 0)},  # Tuesday 7-9 PM
                {'day_of_week': 3, 'start_time': time(18, 0), 'end_time': time(20, 0)},  # Thursday 6-8 PM
                {'day_of_week': 5, 'start_time': time(14, 0), 'end_time': time(18, 0)},  # Saturday 2-6 PM
                {'day_of_week': 6, 'start_time': time(10, 0), 'end_time': time(14, 0)},  # Sunday 10 AM-2 PM
            ]
            
            for avail_data in sample_availabilities:
                availability, created = MentorAvailability.objects.get_or_create(
                    mentor=mentor_profile,
                    day_of_week=avail_data['day_of_week'],
                    start_time=avail_data['start_time'],
                    end_time=avail_data['end_time'],
                    defaults={'is_booked': False}
                )
                if created:
                    print(f"Created availability: {availability}")
        else:
            print(f"Mentor profile already exists: {mentor_profile}")

if __name__ == '__main__':
    create_sample_mentors()
    print("Sample mentors and availability created successfully!")
