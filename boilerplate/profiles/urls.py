from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path(r"<str:username>/edit/", views.profile_edit_view, name="profile-edit"),
    path(r"<str:username>/", views.profile_view, name="profile"),
]
