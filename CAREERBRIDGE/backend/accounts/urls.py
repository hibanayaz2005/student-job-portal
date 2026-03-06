from django.urls import path
from .views import (
    RegisterView,
    VerifyOTPView,
    SetPasswordView,
    LoginView,
    MeView,
    ProfileView,
    settings_page,
    login_page,
    logout_page,
    google_login
)

app_name = "accounts"

urlpatterns = [

    # API authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("set-password/", SetPasswordView.as_view(), name="set-password"),
    path("login/", LoginView.as_view(), name="login"),

    # API user data
    path("me/", MeView.as_view(), name="me"),
    path("profile/", ProfileView.as_view(), name="profile"),

    # Web pages
    path("login-page/", login_page, name="login-page"),
    path("settings/", settings_page, name="settings"),
    path("logout/", logout_page, name="logout"),

    # OAuth
    path("google/", google_login, name="google"),
]