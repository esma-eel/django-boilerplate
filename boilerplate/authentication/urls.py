from django.urls import path, include

app_name = "boilerplate.authentication"

urlpatterns = [
    path("api/", include("boilerplate.authentication.api.urls")),
]
