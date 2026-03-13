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

    google_login,
    PasswordResetRequestView,
    password_reset_confirm_page,
    ChangePasswordView

    google_login
)

app_name = "accounts"

urlpatterns = [

    # API authentication
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/<uidb64>/<token>/", password_reset_confirm_page, name="password_reset_confirm"),

    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("set-password/", SetPasswordView.as_view(), name="set-password"),
    path("login/", LoginView.as_view(), name="login"),


    # API user data
    path("me/", MeView.as_view(), name="me"),
    path("profile/", ProfileView.as_view(), name="profile"),

    path("change-password/", ChangePasswordView.as_view(), name="change-password"),



    # Web pages
    path("login-page/", login_page, name="login-page"),
    path("settings/", settings_page, name="settings"),
    path("logout/", logout_page, name="logout"),

    # OAuth
    path("google/", google_login, name="google"),
]