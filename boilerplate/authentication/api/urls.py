from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .login import views as login_views
from .blacklist import views as blacklist_views
from .password import views as password_views


login_urlpatterns = [
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
        "jwt/create-phone/",
        login_views.JWTCreateWithPhoneNumberAndPassword.as_view(),
        name="jwt-create-phone",
    ),
    path(
        "jwt/create-phone-otp/",
        login_views.JWTCreateWithPhoneNumberAndOTPView.as_view(),
        name="jwt-create-phone-otp",
    ),
    path(
        "jwt/create-email/",
        login_views.JWTCreateWithEmailAndPassword.as_view(),
        name="jwt-create-email",
    ),
    path(
        "jwt/create-email-otp/",
        login_views.JWTCreateWithEmailAndOTPView.as_view(),
        name="jwt-create-email-otp",
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
]

blacklist_urlpatterns = [
    # blacklist
    path(
        "jwt/blacklist/",
        blacklist_views.JWTTokenBlacklistView.as_view(),
        name="jwt-blacklist",
    ),
    path(
        "token/blacklist/",
        blacklist_views.SlidingTokenBlacklistView.as_view(),
        name="token-blacklist",
    ),
]

password_urlpatterns = [
    path(
        "reset-password/phone-otp/",
        password_views.ResetPasswordOTPWithPhoneNumberView.as_view(),
        name="reset-password-phone-otp",
    ),
    # otl
    path(
        "reset-password/request/email-otl/",
        password_views.ResetPasswordRequestOTLWithEmailView.as_view(),
        name="reset-password-request-email-otl",
    ),
    path(
        "reset-password/email-otl/<str:otl>/",
        password_views.ResetPasswordOTLWithEmailView.as_view(),
        name="reset-password-email-otl",
    ),
    path(
        "change-password/",
        password_views.AuthenticatedUserChangePassword.as_view(),
        name="change-password",
    ),
]

urlpatterns = (
    [] + login_urlpatterns + blacklist_urlpatterns + password_urlpatterns
)
