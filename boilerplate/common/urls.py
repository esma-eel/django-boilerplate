from django.urls import path, include

app_name = "common"

urlpatterns = [
    path("api/", include("boilerplate.common.api.urls")),
]
