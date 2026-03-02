from django.urls import path
from .views import JobListView, JobCreateView, ApplyJobView

urlpatterns = [
    path('', JobListView.as_view(), name='jobs-list'),
    path('post/', JobCreateView.as_view(), name='jobs-post'),
    path('apply/', ApplyJobView.as_view(), name='jobs-apply'),
]
