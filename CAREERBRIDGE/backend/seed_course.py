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

    # create a professional test with 10 questions for Web Development
    questions = [
        {
            "question": "What is the primary role of CSS in web development?",
            "options": ["Structuring the document", "Styling and visual layout", "Server-side logic", "Database management"],
            "correct_index": 1,
            "explanation": "CSS (Cascading Style Sheets) is used for styling and visually formatting the HTML elements on a page."
        },
        {
            "question": "Which of the following describes a 'Full Stack' developer?",
            "options": ["A developer who only writes HTML", "A developer who configures cloud servers", "A developer who works on both frontend and backend technologies", "A database administrator"],
            "correct_index": 2,
            "explanation": "A Full Stack developer possesses knowledge of both client-side and server-side components of web applications."
        },
        {
            "question": "What does a 'RESTful' API typically use for transferring data?",
            "options": ["XML", "SOAP", "FTP", "JSON"],
            "correct_index": 3,
            "explanation": "JSON is relatively lightweight and human-readable, making it the most common data format employed when designing REST API services."
        },
        {
            "question": "In standard HTTP operations, which method is typically used to update an existing resource?",
            "options": ["GET", "POST", "PUT", "DELETE"],
            "correct_index": 2,
            "explanation": "The HTTP PUT method is typically used to update an existing resource by replacing its contents."
        },
        {
            "question": "Which array method in JavaScript creates a new array populated with the results of calling a provided function on every element in the calling array?",
            "options": ["Array.filter()", "Array.map()", "Array.reduce()", "Array.push()"],
            "correct_index": 1,
            "explanation": "Array.map() processes every item in the original array and returns a new array with the transformed items."
        }
    ]

    SkillTest.objects.filter(course=course).delete()
    SkillTest.objects.create(
        course=course,
        title="Web Development Essentials Final Assessment",
        description="A 5-question professional assessment testing your knowledge of frontend and backend web fundamentals.",
        passing_score=60,
        time_limit_minutes=15,
        questions=questions
    )
    # Add Lessons
    from courses.models import Lesson
    Lesson.objects.filter(course=course).delete()
    lessons_data = [
        {"title": "Introduction to Web Dev", "url": "https://www.youtube.com/watch?v=nu_pCVPKzTk", "duration": "15m", "order": 1},
        {"title": "HTML Fundamentals", "url": "https://www.youtube.com/watch?v=UB1O30fS-EE", "duration": "45m", "order": 2},
        {"title": "CSS Styling Basics", "url": "https://www.youtube.com/watch?v=yfoY53QXEnI", "duration": "1h 10m", "order": 3},
        {"title": "Advanced Javascript Concepts", "url": "https://www.youtube.com/watch?v=W6NZfCO5SIk", "duration": "2h 30m", "order": 4},
    ]
    for ld in lessons_data:
        Lesson.objects.create(
            course=course,
            title=ld["title"],
            video_url=ld["url"],
            duration=ld["duration"],
            order=ld["order"]
        )

    print("Seeded database with BCA Course, Lessons, and 20-question test!")

if __name__ == "__main__":
    seed()
