from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views


urlpatterns = [
    # simple jwt
    path(
        "jwt/create/",
        jwt_views.TokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path(
        "jwt/refresh/", jwt_views.TokenRefreshView.as_view(), name="jwt-refresh"
    ),
    path("jwt/verify/", jwt_views.TokenVerifyView.as_view(), name="jwt-verify"),
    # boilerplate
    path(
        "jwt/phone-number-and-password/",
        views.JWTCreateWithPhoneNumberAndPassword.as_view(),
        name="jwt-phone-number-and-password",
    ),
    path(
        "jwt/email-and-password/",
        views.JWTCreateWithEmailAndPassword.as_view(),
        name="jwt-email-and-password",
    ),
]
