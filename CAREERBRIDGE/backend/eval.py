import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careerbridge.settings')
django.setup()

from django.test import Client
from accounts.models import User

c = Client()
u = User.objects.first()
if u:
    print("User is:", u.username, u.first_name)
    c.force_login(u)
    res = c.get('/', HTTP_HOST='localhost')
    content = res.content.decode('utf-8')
    
    import re
    match1 = re.search(r'Welcome back.*?👋', content, re.DOTALL)
    if match1:
        print("Welcome matched:", match1.group().encode('ascii', 'replace').decode('ascii'))
    
    match2 = re.search(r'<div class="user-name">(.*?)</div>', content)
    if match2:
        print("User Name matched:", match2.group(1).encode('ascii', 'replace').decode('ascii'))
else:
    print("No user found")
