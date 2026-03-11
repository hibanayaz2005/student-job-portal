"""
URL configuration for careerbridge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_page, settings_page, logout_page, RegisterView

urlpatterns = [
    path('', include('dashboard.urls')),
    path('admin/', admin.site.urls),

    # Simple login page (session-based) used by the frontend
    path('accounts/login/', login_page, name='accounts-login'),
    # session-driven settings/logout (mirror API paths)
    path('accounts/settings/', settings_page, name='accounts-settings'),
    path('accounts/logout/', logout_page, name='accounts-logout'),

    # Authentication
    path('api/auth/', include('accounts.urls')),
    path('api/register', RegisterView.as_view(), name='api-register'),
    path('api/register/', RegisterView.as_view(), name='api-register-slash'),

    # Verification
    path('api/verify/', include('verification.urls')),
    # Resume uploads
    path('api/resume/', include('resume.urls')),
    # Jobs API
    path('api/jobs/', include('jobs.urls')),
    # Mentorship API
    path('api/mentorship/', include('mentorship.urls')),
    # Projects API
    path('api/projects/', include('projects.urls')),
]

# Media files (uploads)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)