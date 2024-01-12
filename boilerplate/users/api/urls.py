from django.urls import path
from . import views

app_name = "api-users"

urlpatterns = [
    path(
        "create/",
        views.UserCreateAPIView.as_view(),
        name="user-create",
    )
]
