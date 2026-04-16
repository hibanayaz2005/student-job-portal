from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_courses, name='list_courses'),
    path('<int:course_id>/', views.get_course, name='get_course'),
    path('<int:course_id>/test/', views.get_test, name='get_test'),
    path('<int:course_id>/test/submit/', views.submit_test, name='submit_test'),
]
