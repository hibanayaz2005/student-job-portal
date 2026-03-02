from django.urls import path
from .views import RegisterView, LoginView, MeView, ProfileView, settings_page, logout_page, google_login

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('me/', MeView.as_view()),
    path('profile/', ProfileView.as_view()),           # API for user/profile data
    path('settings/', settings_page, name='settings'), # web form for profile settings
    path('logout/', logout_page, name='logout'),
    path('google/', google_login, name='google'),
]
