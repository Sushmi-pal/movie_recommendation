from rest_framework import serializers
from .models import Notification
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
