from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    created_at = serializers.DateTimeField()
    seen = serializers.BooleanField(default=False)
    # class Meta:
    #     model = Notification
    #     fields = ['id', 'message', 'user', 'seen', 'created_at']
