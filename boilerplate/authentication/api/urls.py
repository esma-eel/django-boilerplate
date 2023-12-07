from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views


urlpatterns = [
    # JWT
    path(
        "jwt/create/",
        jwt_views.TokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path(
        "jwt/refresh/", jwt_views.TokenRefreshView.as_view(), name="jwt-refresh"
    ),
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
    # TOKEN
    path(
        "token/create/",
        jwt_views.TokenObtainSlidingView.as_view(),
        name="token-create",
    ),
    path(
        "token/refresh/",
        jwt_views.TokenRefreshSlidingView.as_view(),
        name="token-refresh",
    ),
    path(
        "token/verify/",
        jwt_views.TokenVerifyView.as_view(),
        name="token-verify",
    ),
    # blacklist
    path(
        "jwt/blacklist/",
        views.JWTTokenBlacklistView.as_view(),
        name="jwt-blacklist",
    ),
    path(
        "token/blacklist/",
        views.SlidingTokenBlacklistView.as_view(),
        name="token-blacklist",
    ),
]