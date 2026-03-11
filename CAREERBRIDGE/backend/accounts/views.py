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
from .models import Student


def register_student(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if Student.objects.filter(email=email).exists():
            return render(request, "accounts/login.html", {"error": "Email already exists"})

        Student.objects.create(
            email=email,
            password=make_password(password)
        )

        return redirect("login")

    return render(request, "accounts/register.html")


def login_student(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            student = Student.objects.get(email=email)

            if check_password(password, student.password):
                request.session["student"] = student.email
                return redirect("dashboard")

        except Student.DoesNotExist:
            pass

    return render(request, "accounts/login.html")
# =========================
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
        
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        username = email.split('@')[0]
        # Prevent username conflict
        if User.objects.filter(username=username).exists():
            username = f"{username}_{random.randint(1000,9999)}"

        user = User(username=username, email=email, first_name=name, phone=phone, role='student')
        # Store hashed password
        user.set_password(password)
        user.save()

        if hasattr(user, 'student_profile'):
            profile = user.student_profile
            profile.college_name = college
            profile.branch = course
            if year and year[0].isdigit():
                profile.year_of_study = int(year[0])
            if skills:
                profile.skills = [s.strip() for s in skills.split(',') if s.strip()]
            profile.save()

        return Response({"message": "Account created successfully", "success": True})


# =========================
# VERIFY OTP
# =========================
class VerifyOTPView(APIView):

    def post(self, request):

        otp = request.data.get("otp")

        session_otp = request.session.get("otp")
        user_id = request.session.get("user_id")

        if not session_otp or not user_id:
            return Response({"error": "Session expired"}, status=400)

        if str(otp) == str(session_otp):

            User = get_user_model()
            user = User.objects.get(id=user_id)

            user.is_active = True
            user.save()

            return Response({"message": "OTP verified. Now set password."})

        return Response({"error": "Invalid OTP"}, status=400)


# =========================
# SET PASSWORD
# =========================
class SetPasswordView(APIView):

    def post(self, request):

        password = request.data.get("password")
        user_id = request.session.get("user_id")

        if not password:
            return Response({"error": "Password required"}, status=400)

        User = get_user_model()

        user = User.objects.get(id=user_id)

        user.set_password(password)
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Password set successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        identifier = request.data.get('email') or request.data.get('identifier')
        password = request.data.get('password')

        if not identifier or not password:
            return Response({'error': 'Email/Username and password required'}, status=400)

        User = get_user_model()
        user = None
        
        # Try finding by email first
        try:
            user = User.objects.get(email__iexact=identifier)
        except User.DoesNotExist:
            # If not found by email, try username
            try:
                user = User.objects.get(username__iexact=identifier)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=401)

        # Compare password
        valid = user.check_password(password)
        if not valid:
            return Response({'error': 'Invalid password'}, status=401)

        # Secure authentication
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'success': True,
            'message': 'Login successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
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
