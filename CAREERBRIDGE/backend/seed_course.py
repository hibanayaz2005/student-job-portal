import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')
django.setup()

from courses.models import Course, SkillTest

def seed():
    # Create BCA course
    course, _ = Course.objects.get_or_create(
        title="Web Development for BCA",
        provider="CareerBridge",
        provider_url="https://www.youtube.com/watch?v=nu_pCVPKzTk",
        category="web",
        target_program="BCA",
        is_free=True,
        description="Comprehensive web development for BCA students.",
        duration="4 weeks",
        icon="🌐"
    )

    # create a test with 20 questions
    questions = []
    for i in range(1, 21):
        questions.append({
            "question": f"Sample Question {i} for BCA Web Dev. What is 2 + {i}?",
            "options": [f"{2+i}", f"{2+i+1}", f"{2+i+2}", "None of the above"],
            "correct_index": 0,
            "explanation": f"Basic math, {2} + {i} = {2+i}"
        })

    SkillTest.objects.filter(course=course).delete()
    SkillTest.objects.create(
        course=course,
        title="BCA Web Dev Final Assessment",
        description="A 20-question comprehensive assessment.",
        passing_score=70,
        time_limit_minutes=30,
        questions=questions
    )
    print("Seeded database with BCA Course and 20-question test!")

if __name__ == "__main__":
    seed()
