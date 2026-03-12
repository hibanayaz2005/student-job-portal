from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import MentorProfile, MentorAvailability, MentorSession
from accounts.models import StudentProfile


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def mentor_list(request):
    """Get list of available mentors with their availability status."""
    mentors = MentorProfile.objects.filter(is_approved=True, is_available=True)
    
    mentor_data = []
    for mentor in mentors:
        # Get current week availability
        current_day = timezone.now().weekday()
        availabilities = MentorAvailability.objects.filter(
            mentor=mentor,
            day_of_week=current_day,
            is_booked=False
        )
        
        mentor_data.append({
            'id': mentor.id,
            'name': mentor.user.get_full_name() or mentor.user.username,
            'mentor_type': mentor.mentor_type,
            'expertise': mentor.expertise,
            'bio': mentor.bio,
            'company': mentor.company,
            'designation': mentor.designation,
            'years_experience': mentor.years_experience,
            'rating': mentor.rating,
            'sessions_completed': mentor.sessions_completed,
            'hourly_rate': mentor.hourly_rate,
            'is_available': mentor.is_available,
            'today_available': availabilities.exists(),
            'today_slots': [
                {
                    'start_time': slot.start_time.strftime('%H:%M'),
                    'end_time': slot.end_time.strftime('%H:%M')
                }
                for slot in availabilities
            ]
        })
    
    return Response({'mentors': mentor_data})


@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def mentor_availability(request, mentor_id):
    """Get detailed availability for a specific mentor."""
    mentor = get_object_or_404(MentorProfile, id=mentor_id)
    
    # Get availability for the next 7 days
    availabilities = []
    today = timezone.now().date()
    
    for i in range(7):
        date = today + timedelta(days=i)
        day_of_week = date.weekday()
        
        day_slots = MentorAvailability.objects.filter(
            mentor=mentor,
            day_of_week=day_of_week,
            is_booked=False
        )
        
        if day_slots.exists():
            availabilities.append({
                'date': date.strftime('%Y-%m-%d'),
                'day_name': date.strftime('%A'),
                'slots': [
                    {
                        'id': slot.id,
                        'start_time': slot.start_time.strftime('%H:%M'),
                        'end_time': slot.end_time.strftime('%H:%M')
                    }
                    for slot in day_slots
                ]
            })
    
    return Response({
        'mentor': {
            'id': mentor.id,
            'name': mentor.user.get_full_name() or mentor.user.username,
            'is_available': mentor.is_available
        },
        'availability': availabilities
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_http_methods(["POST"])
def book_session(request):
    """Book a mentorship session."""
    try:
        data = json.loads(request.body)
        mentor_id = data.get('mentor_id')
        availability_id = data.get('availability_id')
        topic = data.get('topic')
        session_type = data.get('session_type', 'video')
        session_date = data.get('session_date')
        
        # Get student profile
        try:
            student = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            return Response(
                {'error': 'Student profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get mentor and availability
        mentor = get_object_or_404(MentorProfile, id=mentor_id)
        availability = get_object_or_404(MentorAvailability, id=availability_id, mentor=mentor)
        
        # Check if availability is still available
        if availability.is_booked:
            return Response(
                {'error': 'This time slot is already booked'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Parse session date
        try:
            session_datetime = datetime.fromisoformat(session_date.replace('Z', '+00:00'))
        except ValueError:
            return Response(
                {'error': 'Invalid date format'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create session
        session = MentorSession.objects.create(
            mentor=mentor,
            student=student,
            topic=topic,
            session_type=session_type,
            session_date=session_datetime,
            status='pending'
        )
        
        # Mark availability as booked
        availability.is_booked = True
        availability.save()
        
        return Response({
            'message': 'Session booked successfully',
            'session_id': session.id,
            'status': session.status
        }, status=status.HTTP_201_CREATED)
        
    except json.JSONDecodeError:
        return Response(
            {'error': 'Invalid JSON data'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_sessions(request):
    """Get current user's mentorship sessions."""
    user = request.user
    
    try:
        student = StudentProfile.objects.get(user=user)
        sessions = MentorSession.objects.filter(student=student).order_by('-created_at')
    except StudentProfile.DoesNotExist:
        # Check if user is a mentor
        try:
            mentor = MentorProfile.objects.get(user=user)
            sessions = MentorSession.objects.filter(mentor=mentor).order_by('-created_at')
        except MentorProfile.DoesNotExist:
            return Response({'sessions': []})
    
    session_data = []
    for session in sessions:
        session_data.append({
            'id': session.id,
            'topic': session.topic,
            'session_type': session.session_type,
            'session_date': session.session_date.isoformat(),
            'duration_minutes': session.duration_minutes,
            'status': session.status,
            'payment_status': session.payment_status,
            'meeting_link': session.meeting_link,
            'notes': session.notes,
            'mentor': {
                'name': session.mentor.user.get_full_name() or session.mentor.user.username,
                'expertise': session.mentor.expertise
            } if hasattr(session, 'student') else None,
            'student': {
                'name': session.student.user.get_full_name() or session.student.user.username,
                'college_name': session.student.college_name
            } if hasattr(session, 'mentor') else None,
            'created_at': session.created_at.isoformat()
        })
    
    return Response({'sessions': session_data})
