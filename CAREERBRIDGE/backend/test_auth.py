import requests

s = requests.Session()
r1 = s.post('http://127.0.0.1:8000/api/register/', json={
    'name': 'Test',
    'email': 'test4@e.com',
    'password': 'password123',
    'phone': '',
    'college': '',
    'course': '',
    'year': '',
    'skills': '',
})
print("Register response:", r1.json())

r2 = s.post('http://127.0.0.1:8000/api/auth/login/', json={
    'email': 'test4@e.com',
    'password': 'password123'
})
print("Login response:", r2.json())
print("Cookies:", s.cookies.get_dict())

r3 = s.get('http://127.0.0.1:8000/')
print("Is auth-overlay hidden?", 'class="hidden"' in r3.text)
