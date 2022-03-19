from rest_framework import serializers
from .models import Notification
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class NotificationSerializer(serializers.ModelSerializer):
    # message = serializers.CharField(max_length=1000)
    # created_at = serializers.DateTimeField()
    # seen = serializers.BooleanField(default=False)
    # username = serializers.ReadOnlyField()
    class Meta:
        model = Notification
        fields = '__all__'
