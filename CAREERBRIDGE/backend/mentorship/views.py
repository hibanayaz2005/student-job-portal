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
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings

from .models import MentorProfile, MentorAvailability, MentorSession
from accounts.models import StudentProfile
from dashboard.models import Notification


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
            'user_id': mentor.user_id,
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
            'phone_number': mentor.phone_number,
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
        data = request.data
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
        
        # Get mentor
        mentor = get_object_or_404(MentorProfile, id=mentor_id)
        
        # Check approval
        if not mentor.is_approved:
            return Response(
                {'error': 'This mentor is pending verification and cannot accept bookings yet.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        # Optional availability check
        if availability_id:
            availability = get_object_or_404(MentorAvailability, id=availability_id, mentor=mentor)
            if availability.is_booked:
                return Response(
                    {'error': 'This time slot is already booked'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Mark availability as booked
            availability.is_booked = True
            availability.save()
        
        # Parse session date
        try:
            session_datetime = datetime.fromisoformat(session_date.replace('Z', '+00:00'))
        except ValueError:
            return Response(
                {'error': 'Invalid date format'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        duration_minutes = data.get('duration_minutes', 60)
        notes = data.get('notes', '')

        # Create session
        session = MentorSession.objects.create(
            mentor=mentor,
            student=student,
            topic=topic,
            session_type=session_type,
            session_date=session_datetime,
            duration_minutes=duration_minutes,
            notes=notes,
            status='pending'
        )
        
        # Real-time Notification
        channel_layer = get_channel_layer()
        student_name = request.user.get_full_name() or request.user.username
        booking_time = session_datetime.strftime("%Y-%m-%d %I:%M %p")
        message_details = notes if notes else "No additional notes provided."
        
        notification_title = f"New Session Request from {student_name}"
        notification_msg = f"{student_name} has requested a {session_type} session for {booking_time}. Message: {message_details}"
        
        # Create dashboard notification
        Notification.objects.create(
            user=mentor.user,
            title=notification_title,
            message=notification_msg
        )
        
        is_online = cache.get(f"user_online_{mentor.user.id}")
        
        # Send WebSocket notification to mentor
        async_to_sync(channel_layer.group_send)(
            f"user_notifications_{mentor.user.id}",
            {
                "type": "send_notification",
                "data": {
                    "type": "session_booked",
                    "title": notification_title,
                    "message": notification_msg,
                    "session_id": session.id,
                    "student_name": student_name,
                    "session_type": session_type,
                    "booking_time": booking_time,
                    "open_chat": is_online and True or False,
                    "peer_id": request.user.id
                }
            }
        )
        
        # Also notify the student themselves about the booking update
        async_to_sync(channel_layer.group_send)(
            f"user_notifications_{request.user.id}",
            {
                "type": "send_notification",
                "data": {
                    "type": "booking_status_update",
                    "session_id": session.id,
                    "status": session.status
                }
            }
        )

        if not is_online:
            # Email alert if offline
            if mentor.user.email:
                try:
                    send_mail(
                        notification_title,
                        notification_msg,
                        settings.DEFAULT_FROM_EMAIL,
                        [mentor.user.email],
                        fail_silently=True,
                    )
                except Exception as e:
                    print("Error sending email:", e)
        
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
    """Get current user's mentorship sessions (both as student and mentor)."""
    user = request.user
    sessions = MentorSession.objects.none()
    
    # Get sessions as a student
    try:
        student = StudentProfile.objects.get(user=user)
        sessions = sessions | MentorSession.objects.filter(student=student)
    except StudentProfile.DoesNotExist:
        pass
        
    # Get sessions as a mentor
    try:
        mentor = MentorProfile.objects.get(user=user)
        sessions = sessions | MentorSession.objects.filter(mentor=mentor)
    except MentorProfile.DoesNotExist:
        mentor = None

    sessions = sessions.distinct().order_by('-created_at')
    
    session_data = []
    for session in sessions:
        is_mentor_role = (mentor and session.mentor == mentor)
        
        session_data.append({
            'id': session.id,
            'role': 'mentor' if is_mentor_role else 'student',
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
            },
            'student': {
                'name': session.student.user.get_full_name() or session.student.user.username,
                'college_name': session.student.college_name
            },
            'created_at': session.created_at.isoformat()
        })
    
    # Include mentor profile status
    mentor_status = None
    if mentor:
        mentor_status = {
            'is_approved': mentor.is_approved,
            'mentor_type': mentor.mentor_type,
            'company': mentor.company
        }
        
    return Response({
        'sessions': session_data,
        'mentor_status': mentor_status
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history(request, peer_id):
    from mentorship.models import Message
    from django.db.models import Q
    msgs = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver_id=peer_id)) |
        (Q(sender_id=peer_id) & Q(receiver=request.user))
    ).select_related('sender').order_by('created_at')[:100]

    data = [
        {
            'sender_id': m.sender_id,
            'sender_name': m.sender.get_full_name() or m.sender.username,
            'message': m.text,
            'timestamp': m.created_at.strftime('%H:%M'),
            'is_mine': m.sender_id == request.user.id,
        }
        for m in msgs
    ]
    return Response({'messages': data, 'peer_id': peer_id, 'my_id': request.user.id})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_peer_user_id(request, mentor_profile_id):
    mentor = get_object_or_404(MentorProfile, id=mentor_profile_id)
    return Response({
        'user_id': mentor.user_id,
        'name': mentor.user.get_full_name() or mentor.user.username,
        'username': mentor.user.username,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_mentor(request):
    """Apply to become a mentor, uploading a college ID."""
    user = request.user
    if hasattr(user, 'mentor_profile'):
        return Response({'error': 'You have already applied or are already a mentor.'}, status=400)
        
    college_id_file = request.FILES.get('college_id')
    if not college_id_file:
        return Response({'error': 'College ID document is required for verification.'}, status=400)
        
    full_name = request.POST.get('full_name', '')
    if full_name:
        parts = full_name.split(' ', 1)
        user.first_name = parts[0]
        if len(parts) > 1:
            user.last_name = parts[1]
        user.save()
    
    mentor_type = request.POST.get('mentor_type', 'senior')
    company = request.POST.get('company', '')
    designation = request.POST.get('designation', '')
    expertise_str = request.POST.get('expertise', '')
    
    # ID Verification via PDF parsing or Image check
    is_auto_verified = False
    try:
        if college_id_file.name.lower().endswith('.pdf'):
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(college_id_file)
            id_text = ""
            for page in pdf_reader.pages:
                id_text += (page.extract_text() or "") + " "
            id_text_low = id_text.lower()
            
            if id_text_low.strip():
                if mentor_type in ['senior', 'alumni']:
                    keywords = ['university', 'college', 'institute', 'b.tech', 'bca', 'technology', 'academy', 'student', 'id card', 'enrollment']
                    if (company and company.lower() in id_text_low) or any(kw in id_text_low for kw in keywords):
                        is_auto_verified = True
                else:
                    exp_found = any(e.strip().lower() in id_text_low for e in expertise_str.split(',') if e.strip())
                    if (company and company.lower() in id_text_low) or (designation and designation.lower() in id_text_low) or exp_found:
                        is_auto_verified = True
            else:
                # Scanned PDF or no text found - allow for manual review
                is_auto_verified = False
        else:
            # It's an image (JPG/PNG) - allow for manual review
            is_auto_verified = False
            
        # Reset pointer so it gets saved to model properly
        college_id_file.seek(0)
    except Exception as e:
        # If processing fails, we still allow submission for manual review
        is_auto_verified = False
        college_id_file.seek(0)

    expertise = [e.strip() for e in expertise_str.split(',') if e.strip()]

    try:
        years_exp = int(request.POST.get('years_experience', 0) or 0)
    except (ValueError, TypeError):
        years_exp = 0

    try:
        mentor = MentorProfile.objects.create(
            user=user,
            mentor_type=request.POST.get('mentor_type', 'senior'),
            company=request.POST.get('company', ''),
            designation=request.POST.get('designation', ''),
            years_experience=years_exp,
            bio=request.POST.get('bio', ''),
            expertise=expertise,
            college_id=college_id_file,
            phone_number=request.POST.get('phone_number', ''),
            is_approved=True  # Instant verification
        )
    except Exception as e:
        return Response({'error': f'Failed to create mentor profile: {str(e)}'}, status=500)

    return Response({'message': 'Application approved instantly! You are now a verified mentor.'}, status=201)
