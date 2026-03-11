import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()
with open('users_utf8.txt', 'w', encoding='utf-8') as f:
    for u in users:
        f.write(f"ID: {u.id}, Username: '{u.username}', Email: '{u.email}', PasswordHash: {u.password[:20]}\n")
