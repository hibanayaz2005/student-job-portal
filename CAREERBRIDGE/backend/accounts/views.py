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


# =========================
# REGISTER
# =========================
class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save(is_active=False)

            otp = random.randint(100000, 999999)

            request.session['otp'] = str(otp)
            request.session['user_id'] = user.id

            send_mail(
                "CareerBridge Verification Code",
                f"Your verification code is {otp}",
                "noreply@careerbridge.com",
                [user.email],
                fail_silently=False,
            )

            return Response({
                "message": "User created. OTP sent to email."
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # simple validation
        if not username or not password:
            return Response({'error': 'username and password required'}, status=400)

        try:
            user = authenticate(username=username, password=password)
        except ValueError as e:
            return Response({'error': str(e)}, status=400)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=401)
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
    """Simple session login page for students/employers."""

    if request.method == 'GET':
        return render(request, 'accounts/login.html')

    # POST request
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        messages.error(request, 'Please provide username and password')
        return render(request, 'accounts/login.html')

    # authenticate user
    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)
        return redirect('/')   # redirect to homepage or dashboard

    messages.error(request, 'Invalid credentials')
    return render(request, 'accounts/login.html')


def logout_page(request):
    """Log the user out of the session and redirect to login."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts-login')


def google_login(request):
    """Stub view for Google OAuth sign‑in.

    In a real deployment this would redirect to Google's OAuth endpoint and
    handle the callback. For now it simply returns a placeholder message.
    """
    return HttpResponse("Google sign-in is not configured yet.")
