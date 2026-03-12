import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model
from accounts.models import User, StudentProfile

# 1. Try to create a test user
test_email = 'test_login_1@example.com'
test_pass = 'TestPass123!'
test_username = 'test_login_1'

# Cleanup
User.objects.filter(email=test_email).delete()

print(f"Creating user {test_username} with email {test_email}")
user = User.objects.create_user(
    username=test_username,
    email=test_email,
    password=test_pass,
    role='student'
)
print(f"User created. ID: {user.id}")

# 2. Try standard authenticate with email
print(f"Authenticating with email: {test_email}")
auth_user = authenticate(username=test_email, password=test_pass)
if auth_user:
    print(f"SUCCESS: Authenticated as {auth_user.username}")
else:
    print("FAILED: Could not authenticate with email")

# 3. Try standard authenticate with username
print(f"Authenticating with username: {test_username}")
auth_user_2 = authenticate(username=test_username, password=test_pass)
if auth_user_2:
    print(f"SUCCESS: Authenticated as {auth_user_2.username}")
else:
    print("FAILED: Could not authenticate with username")
