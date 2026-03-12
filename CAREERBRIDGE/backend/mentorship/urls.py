from django.urls import path
from . import views

urlpatterns = [
    path('mentors/', views.mentor_list, name='mentor-list'),
    path('mentors/<int:mentor_id>/availability/', views.mentor_availability, name='mentor-availability'),
    path('book-session/', views.book_session, name='book-session'),
    path('my-sessions/', views.my_sessions, name='my-sessions'),
]
