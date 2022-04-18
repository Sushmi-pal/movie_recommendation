from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class Movies(admin.ModelAdmin):
    list_display = ["message", "user", "seen", "created_at"]
    search_fields = ["user"]
