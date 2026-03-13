from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_portal, name='student_portal'),
    path('student-portal/', views.student_portal, name='student_portal_alias'),
    path("send-aadhaar-otp/", views.send_aadhaar_otp),
    path("verify-aadhaar-otp/", views.verify_aadhaar_otp),
    path("api/notifications/", views.get_notifications),
    path("api/notifications/read/", views.mark_notification_read),

    path('', views.home, name='home'),
    path('student-portal/', views.student_portal, name='student_portal'),

]