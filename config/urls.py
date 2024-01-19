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
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
)


media_url = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
static_url = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


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
    # swagger
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

urlpatterns = urlpatterns + media_url
urlpatterns = urlpatterns + static_url
