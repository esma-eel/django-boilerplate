from django.urls import path
from . import views


urlpatterns = [
    path(
        "verify/phone/",
        views.VerifyPhoneNumberWithOTPView.as_view(),
        name="profile-verify-phone",
    ),
    path(
        "verify/email/",
        views.VerifyEmailWithOTPView.as_view(),
        name="profile-verify-email",
    ),
]
