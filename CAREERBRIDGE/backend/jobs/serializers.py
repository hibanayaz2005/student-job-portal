from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'employer', 'title', 'description', 'job_type', 'eligible_years', 'location', 'deadline', 'created_at']
        read_only_fields = ['id', 'employer', 'created_at']


from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'student', 'job', 'status', 'applied_at']
        read_only_fields = ['id', 'student', 'status', 'applied_at']
