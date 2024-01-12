"""
URL configuration for django_boilerplate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # mtv
    path("admin/", admin.site.urls),
    path("common/", include("boilerplate.common.urls")),
    path("auth/", include("boilerplate.authentication.urls")),
    path("profiles/", include("boilerplate.profiles.urls")),
    path("users/", include("boilerplate.users.urls")),
    # api
    path("api/common/", include("boilerplate.common.api.urls")),
    path("api/auth/", include("boilerplate.authentication.api.urls")),
    path("api/profiles/", include("boilerplate.profiles.api.urls")),
    path("api/users/", include("boilerplate.users.api.urls")),
]
