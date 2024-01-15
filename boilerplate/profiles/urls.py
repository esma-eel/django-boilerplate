from django.urls import path, include
from . import views

app_name = "profiles"

urlpatterns = [
    path(r"", views.profile_view, name="profile-home"),
    path(r"<str:username>/", views.profile_view, name="profile"),
]
