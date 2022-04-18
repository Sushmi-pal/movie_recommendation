from django.contrib import admin
from .models import Movies, History


@admin.register(Movies)
class Movies(admin.ModelAdmin):
    list_display = ["name", "cast", "category", "url"]
    search_fields = ["name"]


@admin.register(History)
class Movies(admin.ModelAdmin):
    list_display = ["user", "movie", "created_at"]
    search_fields = ["user"]
