from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('student-portal/', views.student_portal, name='student_portal'),
]