from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NotificationSerializer
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@api_view(['GET'])
@csrf_exempt
def get_notifications(request):
    if request.method == "GET":
        notifications = Notification.objects.all()
        print("notifications", notifications)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@csrf_exempt
def get_notifications_click(request):
    if request.method == "GET":
        notifications = Notification.objects.all()
        for i in notifications:
            i.seen = True
            i.save()
        print("notifications", notifications)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
