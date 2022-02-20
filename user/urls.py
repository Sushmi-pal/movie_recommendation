from django.urls import path
from .views import get_started, ProfileView, LoginView, SignupView, LogoutView
urlpatterns=[
    path("get_started/", get_started, name="get_started"),
    path("profile/", ProfileView, name="profile"),
    path("signup/", SignupView, name="signup"),
    path("login/", LoginView, name="signin"),
    path("logout/", LogoutView, name="logout")
]