"""
WSGI config for careerbridge project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')

application = get_wsgi_application()

import time
import sys

max_retries = 5
for i in range(max_retries):
    try:
        call_command('migrate', interactive=False)
        print("Migrations applied successfully!")
        break
    except Exception as e:
        print(f"Migration failed during startup (attempt {i+1}/{max_retries}): {e}")
        if "database is locked" in str(e).lower() or "operationalerror" in str(e).lower():
            time.sleep(2)  # Wait for the other worker to finish migrating
        else:
            break

