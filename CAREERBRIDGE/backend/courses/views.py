import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course, CourseProgress, SkillTest, TestAttempt, Certificate
from accounts.models import StudentProfile


@api_view(['GET'])
def list_courses(request):
    """List all available courses. Optionally filter by target_program."""
    program_filter = request.GET.get('program', '')
    if program_filter and program_filter != 'all':
        courses = Course.objects.filter(target_program__in=[program_filter, 'Any'])
    else:
        courses = Course.objects.all()

    data = []
    for c in courses:
        data.append({
            'id': c.id,
            'title': c.title,
            'provider': c.provider,
            'provider_url': c.provider_url,
            'category': c.category,
            'target_program': c.target_program,
            'target_years': c.target_years,
            'is_free': c.is_free,
            'description': c.description,
            'duration': c.duration,
            'icon': c.icon,
        })
    return Response({'courses': data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_test(request, course_id):
    """Get test questions for a course (without answers)."""
    course = get_object_or_404(Course, id=course_id)
    if not hasattr(course, 'skill_test'):
        return Response({'error': 'No test available for this course.'}, status=404)
        
    test = course.skill_test
    
    # Strip correct answers to prevent cheating
    safe_questions = []
    for idx, q in enumerate(test.questions):
        safe_questions.append({
            'id': idx,
            'question': q.get('question'),
            'options': q.get('options')
        })
        
    return Response({
        'test_id': test.id,
        'title': test.title,
        'description': test.description,
        'passing_score': test.passing_score,
        'time_limit_minutes': test.time_limit_minutes,
        'questions': safe_questions,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_test(request, course_id):
    """Submit test answers, calculate score, and issue certificate if passed."""
    try:
        student_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return Response({'error': 'User is not a student.'}, status=403)

    course = get_object_or_404(Course, id=course_id)
    if not hasattr(course, 'skill_test'):
        return Response({'error': 'No test available.'}, status=404)
        
    test = course.skill_test
    
    try:
        data = json.loads(request.body)
        answers = data.get('answers', {}) # dict of {question_index: selected_index}
    except json.JSONDecodeError:
        return Response({'error': 'Invalid payload.'}, status=400)
    
    # Calculate score
    correct_count = 0
    total_questions = len(test.questions)
    
    if total_questions == 0:
        return Response({'error': 'Test has no questions.'}, status=400)
        
    for idx, q_data in enumerate(test.questions):
        selected_idx = answers.get(str(idx))
        correct_idx = q_data.get('correct_index')
        if selected_idx is not None and int(selected_idx) == int(correct_idx):
            correct_count += 1
            
    score_percentage = int((correct_count / total_questions) * 100)
    passed = score_percentage >= test.passing_score
    
    # Record attempt
    attempt = TestAttempt.objects.create(
        student=student_profile,
        test=test,
        answers=answers,
        score=score_percentage,
        passed=passed
    )
    
    # Update progress and issue certificate if passed
    progress, _ = CourseProgress.objects.get_or_create(student=student_profile, course=course)
    progress.status = 'completed' if passed else 'in_progress'
    progress.save()
    
    certificate_id = None
    if passed:
        from django.utils.crypto import get_random_string
        cert_id_str = f"CERT_{student_profile.id}_{course.id}_{get_random_string(8)}"
        
        cert, created = Certificate.objects.get_or_create(
            student=request.user,
            test=test,
            defaults={'certificate_id': cert_id_str, 'status': 'issued'}
        )
        certificate_id = cert.certificate_id
        
    return Response({
        'score': score_percentage,
        'passed': passed,
        'correct_count': correct_count,
        'total_questions': total_questions,
        'attempt_id': attempt.id,
        'certificate_id': certificate_id
    })
