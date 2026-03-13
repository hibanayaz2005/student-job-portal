from accounts.models import User, StudentProfile
print(f"User count: {User.objects.all().count()}")
print(f"Profile count: {StudentProfile.objects.all().count()}")
u = User.objects.filter(email='hibanayaz2005@gmail.com').first()
print(f"User exists: {u is not None}")
if u:
    print(f"User profile exists: {hasattr(u, 'student_profile')}")
    if hasattr(u, 'student_profile'):
        print(f"User profile details: {u.student_profile}")
