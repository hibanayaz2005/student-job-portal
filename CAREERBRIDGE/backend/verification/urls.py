from django.urls import path
from .views import SubmitVerificationView, VerificationStatusView

urlpatterns = [
    path('submit/', SubmitVerificationView.as_view()),
    path('status/', VerificationStatusView.as_view()),
]