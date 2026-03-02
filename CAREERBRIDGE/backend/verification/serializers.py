from rest_framework import serializers
from .models import VerificationDocument


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationDocument
        fields = '__all__'
        read_only_fields = ['status', 'uploaded_at', 'student']