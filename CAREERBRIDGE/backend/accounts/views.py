import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
# Django authentication is handled by the API views below
# REGISTER
# =========================
from rest_framework.permissions import IsAuthenticated, AllowAny

# =========================
# REGISTER
# =========================
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name', '')
        phone = request.data.get('phone', '')
        college = request.data.get('college', '')
        course = request.data.get('course', '')
        year = request.data.get('year', '')
        skills = request.data.get('skills', '')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=400)

        User = get_user_model()
        
        if User.objects.filter(email__iexact=email).exists():
            return Response({"error": "A user with this email already exists"}, status=400)

        # Generate a unique username from email
        base_username = email.split('@')[0]
        username = base_username
        while User.objects.filter(username__iexact=username).exists():
            username = f"{base_username}_{random.randint(1000, 9999)}"

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name,
                phone=phone,
                role='student'
            )
            
            # The signal in models.py handles StudentProfile creation, 
            # but we update it with registration details here
            if hasattr(user, 'student_profile'):
                profile = user.student_profile
                profile.college_name = college
                profile.branch = course
                # Map '1st Year' etc to integer
                year_map = {'1st': 1, '2nd': 2, '3rd': 3, '4th': 4, 'Final': 4}
                for k, v in year_map.items():
                    if k in year:
                        profile.year_of_study = v
                        break
                
                if skills:
                    profile.skills = [s.strip() for s in skills.split(',') if s.strip()]
                profile.save()

            return Response({"message": "Account created successfully! Please login.", "success": True}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        identifier = request.data.get('email') or request.data.get('identifier')
        password = request.data.get('password')

        if not identifier or not password:
            return Response({'error': 'Email/Username and password required'}, status=400)

        # Use Django's authenticate which handles backends automatically
        from django.contrib.auth import authenticate
        user = authenticate(request, username=identifier, password=password)
        
        if not user:
            return Response({'error': 'Invalid email/username or password'}, status=401)

        if not user.is_active:
            return Response({'error': 'This account is inactive'}, status=401)

        auth_login(request, user)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'message': 'Welcome back!',
            'user': {
                'username': user.username,
                'email': user.email,
                'name': user.get_full_name(),
                'role': user.role
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

# =========================
# PASSWORD RESET API
# =========================
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=400)
            
        User = get_user_model()
        users = User.objects.filter(email__iexact=email)
        
        if users.exists():
            for user in users:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                protocol = 'https' if request.is_secure() else 'http'
                
                reset_url = f"{protocol}://{domain}/api/auth/password-reset-confirm/{uid}/{token}/"
                
                # In a real app, send actual email. For now, we use Django's console backend.
                subject = "Password Reset Requested - CareerBridge"
                message = f"Hello {user.first_name or user.username},\n\nYou requested a password reset. Click the link below to set a new password:\n\n{reset_url}\n\nIf you didn't request this, please ignore this email."
                
                send_mail(subject, message, None, [user.email])
                
            return Response({"message": "If an account exists with this email, a reset link has been sent.", "success": True})
        
        # Always return success to prevent email enumeration
        return Response({"message": "If an account exists with this email, a reset link has been sent.", "success": True})

def password_reset_confirm_page(request, uidb64, token):
    """HTML page for setting new password after clicking the reset link."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            
            if not new_password or new_password != confirm_password:
                return render(request, 'accounts/password_reset_confirm.html', {
                    'error': 'Passwords do not match or are empty',
                    'validlink': True
                })
                
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Your password has been reset successfully. You can now login.')
            return redirect('/')
            
        return render(request, 'accounts/password_reset_confirm.html', {'validlink': True})
    else:
        return render(request, 'accounts/password_reset_confirm.html', {'validlink': False})
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # return serialized user including nested profile
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ProfileView(APIView):
    """Retrieve or update the logged-in user's profile (and basic info)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        # allow partial updates so clients can send only changed fields
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)


@login_required
def settings_page(request):
    """HTML form for editing user information and profile."""
    user = request.user
    role = user.role
    context = {'user': user, 'role': role}

    if request.method == 'POST':
        # update user fields
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        # optionally update username? skip for simplicity
        user.save()

        if role == 'student' and hasattr(user, 'student_profile'):
            prof = user.student_profile
            prof.college_name = request.POST.get('college_name', prof.college_name)
            prof.branch = request.POST.get('branch', prof.branch)
            prof.year_of_study = request.POST.get('year_of_study', prof.year_of_study)
            prof.graduation_year = request.POST.get('graduation_year', prof.graduation_year)
            # skills stored as JSON list; we can split comma-separated
            skills = request.POST.get('skills')
            if skills is not None:
                prof.skills = [s.strip() for s in skills.split(',') if s.strip()]
            certs = request.POST.get('certifications')
            if certs is not None:
                prof.certifications = [c.strip() for c in certs.split(',') if c.strip()]
            linkedin = request.POST.get('linkedin_url')
            if linkedin is not None:
                prof.linkedin_url = linkedin
            prof.save()
            messages.success(request, 'Profile updated successfully.')
        elif role == 'employer' and hasattr(user, 'employer_profile'):
            prof = user.employer_profile
            prof.company_name = request.POST.get('company_name', prof.company_name)
            prof.company_website = request.POST.get('company_website', prof.company_website)
            prof.industry = request.POST.get('industry', prof.industry)
            prof.save()
            messages.success(request, 'Profile updated successfully.')

        return redirect('accounts:settings')

    return render(request, 'accounts/settings.html', context)


from django.contrib.auth import authenticate, login as auth_login

def login_page(request):
    """Redirects the old session login page to the modern Dashboard SPA."""
    return redirect('/')


def logout_page(request):
    """Log the user out of the session and redirect to login."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('/')


def google_login(request):
    """Stub view for Google OAuth sign‑in.

    In a real deployment this would redirect to Google's OAuth endpoint and
    handle the callback. For now it simply returns a placeholder message.
    """
    return HttpResponse("Google sign-in is not configured yet.")
