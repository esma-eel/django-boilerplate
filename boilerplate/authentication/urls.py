from django.urls import path, include

app_name = "authentication"

urlpatterns = [
    path("api/", include("boilerplate.authentication.api.urls")),
]
