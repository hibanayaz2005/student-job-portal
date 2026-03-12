import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')
django.setup()

from django.contrib.auth import authenticate, get_user_model
from accounts.models import User

test_email = 'login_debug@example.com'
test_pass = 'Secret123!'
test_username = 'debug_user'

# 1. Cleanup
User.objects.filter(email=test_email).delete()
User.objects.filter(username=test_username).delete()

# 2. Create user manually like RegisterView does
# (simulating the create_user call)
print(f"Creating user with email: {test_email}")
user = User.objects.create_user(
    username=test_username,
    email=test_email,
    password=test_pass,
    role='student'
)
print(f"User created. Hashed password starts with: {user.password[:20]}")

# 3. Test EmailAuthBackend specifically
from accounts.backends import EmailAuthBackend
backend = EmailAuthBackend()

print("\n--- Testing EmailAuthBackend ---")
# Test Case 1: Exact email
print(f"1. Exact email '{test_email}':")
u1 = backend.authenticate(None, username=test_email, password=test_pass)
print(f"   Result: {'SUCCESS' if u1 else 'FAILED'}")

# Test Case 2: Mixed case email
mixed_email = test_email.upper()
print(f"2. Mixed case email '{mixed_email}':")
u2 = backend.authenticate(None, username=mixed_email, password=test_pass)
print(f"   Result: {'SUCCESS' if u2 else 'FAILED'}")

# Test Case 3: Username
print(f"3. Username '{test_username}':")
u3 = backend.authenticate(None, username=test_username, password=test_pass)
print(f"   Result: {'SUCCESS' if u3 else 'FAILED'}")

# 4. Test global authenticate
print("\n--- Testing Global Authenticate ---")
u4 = authenticate(username=test_email, password=test_pass)
print(f"   Result (Email): {'SUCCESS' if u4 else 'FAILED'}")

# Check if user is active
if u4:
    print(f"   User is_active: {u4.is_active}")
