from django.contrib import admin
from .models import User, StudentProfile, EmployerProfile

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(EmployerProfile)