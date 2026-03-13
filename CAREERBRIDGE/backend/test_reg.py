import requests
url = "http://127.0.0.1:8000/api/register/"
data = {
    "name": "test user",
    "email": "new_test@example.com",
    "password": "Password123!",
    "phone": "1234567890",
    "college": "Test College",
    "course": "B.Tech",
    "year": "3rd Year",
    "graduation_year": "2026",
    "skills": "python, django"
}
try:
    # We need to get CSRF token first or use a session
    s = requests.Session()
    s.get("http://127.0.0.1:8000/")
    csrf = s.cookies.get('csrftoken')
    r = s.post(url, json=data, headers={'X-CSRFToken': csrf})
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Request failed: {e}")
