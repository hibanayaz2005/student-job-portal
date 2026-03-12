from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile, EmployerProfile

User = get_user_model()


class StudentProfileSerializer(serializers.ModelSerializer):
    completion_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'college_name',
            'branch',
            'year_of_study',
            'graduation_year',
            'skills',
            'certifications',
            'linkedin_url',
            'aptitude_passed',
            'resume_score',
            'is_verified',
            'completion_percentage',
        ]
        read_only_fields = ['resume_score', 'is_verified', 'completion_percentage']
        extra_kwargs = {
            'graduation_year': {'required': False},
            'college_name': {'required': False},
            'branch': {'required': False},
            'year_of_study': {'required': False},
        }

    def to_internal_value(self, data):
        # Handle comma-separated strings for skills and certifications
        if 'skills' in data and isinstance(data['skills'], str):
            data = data.copy()
            data['skills'] = [s.strip() for s in data['skills'].split(',') if s.strip()]
        if 'certifications' in data and isinstance(data['certifications'], str):
            data = data.copy()
            data['certifications'] = [c.strip() for c in data['certifications'].split(',') if c.strip()]
        return super().to_internal_value(data)


class EmployerProfileSerializer(serializers.ModelSerializer):
    completion_percentage = serializers.IntegerField(read_only=True)

    class Meta:
        model = EmployerProfile
        fields = [
            'company_name',
            'company_website',
            'industry',
            'is_verified',
            'completion_percentage',
        ]
        read_only_fields = ['is_verified', 'completion_percentage']
        extra_kwargs = {
            'company_name': {'required': False},
            'industry': {'required': False},
        }


class UserSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(required=False)
    employer_profile = EmployerProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'phone',
            'student_profile',
            'employer_profile',
        ]
        read_only_fields = ['id', 'role']

    def update(self, instance, validated_data):
        student_data = validated_data.pop('student_profile', None)
        employer_data = validated_data.pop('employer_profile', None)

        if student_data:
            if 'certifications' in student_data:
                cert = student_data['certifications']
                if isinstance(cert, str):
                    student_data['certifications'] = [c.strip() for c in cert.split(',') if c.strip()]
            if 'skills' in student_data:
                sk = student_data['skills']
                if isinstance(sk, str):
                    student_data['skills'] = [s.strip() for s in sk.split(',') if s.strip()]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if student_data and hasattr(instance, 'student_profile'):
            for attr, value in student_data.items():
                setattr(instance.student_profile, attr, value)
            instance.student_profile.save()

        if employer_data and hasattr(instance, 'employer_profile'):
            for attr, value in employer_data.items():
                setattr(instance.employer_profile, attr, value)
            instance.employer_profile.save()

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )

        # Create profile based on role
        if user.role == 'student':
            StudentProfile.objects.create(user=user, college_name="", branch="", year_of_study=1, graduation_year=2026)
        elif user.role == 'employer':
            EmployerProfile.objects.create(user=user, company_name="", industry="")

        return user