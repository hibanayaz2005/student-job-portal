import requests

url = "http://127.0.0.1:8000/api/register/"
data = {
    "name": "Test User",
    "email": "test_script@example.com",
    "password": "TestPassword123!",
    "phone": "1234567890",
    "college": "Test College",
    "course": "Test Course",
    "year": "4th Year",
    "graduation_year": "2026",
    "linkedin": "https://linkedin.com/in/test",
    "skills": "Python, Django"
}

# First get a CSRF token
session = requests.Session()
session.get("http://127.0.0.1:8000/")
csrf_token = session.cookies.get('csrftoken')

headers = {
    "X-CSRFToken": csrf_token,
    "Content-Type": "application/json"
}

print(f"Sending registration request with CSRF: {csrf_token}")
response = session.post(url, json=data, headers=headers)

print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.json()}")
