from django.urls import path, include

app_name = "profiles"

urlpatterns = [
    path("api/", include("boilerplate.profiles.api.urls")),
]
