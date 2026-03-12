from django.urls import path
from .views import (
    RegisterView,
<<<<<<< HEAD
=======
    VerifyOTPView,
    SetPasswordView,
>>>>>>> 0b0f1a661d9fad69408034b791d0366a517855f9
    LoginView,
    MeView,
    ProfileView,
    settings_page,
    login_page,
    logout_page,
<<<<<<< HEAD
    google_login,
    PasswordResetRequestView,
    password_reset_confirm_page,
    ChangePasswordView
=======
    google_login
>>>>>>> 0b0f1a661d9fad69408034b791d0366a517855f9
)

app_name = "accounts"

urlpatterns = [

    # API authentication
    path("register/", RegisterView.as_view(), name="register"),
<<<<<<< HEAD
    path("login/", LoginView.as_view(), name="login"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path("password-reset-confirm/<uidb64>/<token>/", password_reset_confirm_page, name="password_reset_confirm"),
=======
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("set-password/", SetPasswordView.as_view(), name="set-password"),
    path("login/", LoginView.as_view(), name="login"),
>>>>>>> 0b0f1a661d9fad69408034b791d0366a517855f9

    # API user data
    path("me/", MeView.as_view(), name="me"),
    path("profile/", ProfileView.as_view(), name="profile"),
<<<<<<< HEAD
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
=======
>>>>>>> 0b0f1a661d9fad69408034b791d0366a517855f9

    # Web pages
    path("login-page/", login_page, name="login-page"),
    path("settings/", settings_page, name="settings"),
    path("logout/", logout_page, name="logout"),

    # OAuth
    path("google/", google_login, name="google"),
]