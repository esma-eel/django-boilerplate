from django.urls import path
from .views import UserCreateView

app_name = "users"
urlpatterns = [
    path("create/", UserCreateView.as_view(), name="user-create"),
]
