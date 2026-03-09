from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student-portal/', views.student_portal, name='student_portal'),
    path("send-aadhaar-otp/", views.send_aadhaar_otp),
path("verify-aadhaar-otp/", views.verify_aadhaar_otp),
]