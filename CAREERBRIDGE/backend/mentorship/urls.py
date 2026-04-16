from django.urls import path
from . import views

urlpatterns = [
    path('mentors/', views.mentor_list, name='mentor-list'),
    path('mentors/<int:mentor_id>/availability/', views.mentor_availability, name='mentor-availability'),
    path('book-session/', views.book_session, name='book-session'),
    path('my-sessions/', views.my_sessions, name='my-sessions'),
    path('chat/history/<int:peer_id>/', views.chat_history, name='chat-history'),
    path('chat/peer/<int:mentor_profile_id>/', views.get_peer_user_id, name='peer-user-id'),
    path('apply/', views.apply_mentor, name='apply-mentor'),
]
