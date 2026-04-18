from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_portal, name='student_portal'),
    path('student-portal/', views.student_portal, name='student_portal_alias'),
    path("send-aadhaar-otp/", views.send_aadhaar_otp),
    path("verify-aadhaar-otp/", views.verify_aadhaar_otp),
    path("api/notifications/", views.get_notifications),
    path("api/notifications/read/", views.mark_notification_read),
    
    # Course Dashboard APIs
    path("api/leaderboard/", views.leaderboard_view),
    path("api/dashboard/stats/", views.dashboard_stats_view),
    path("analytics/", views.analytics_dashboard, name='analytics_dashboard'),
    path("real-time-jobs/", views.get_realtime_jobs, name='real_time_jobs'),
]