from django.urls import path
from . import views

app_name = "api-profiles"

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
