from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path(
        r"send-otp-to-verify-phone-number/",
        views.send_otp_to_profile_phone_number_view,
        name="send-otp-to-verify-phone-number",
    ),
    path(
        r"verify-phone-number/",
        views.verify_profile_phone_number_view,
        name="verify-phone-number",
    ),
    path(
        r"send-otp-to-verify-email/",
        views.send_otp_to_profile_email_view,
        name="send-otp-to-verify-email",
    ),
    path(
        r"verify-email/",
        views.verify_profile_email_view,
        name="verify-email",
    ),
    path(
        r"<str:username>/",
        views.ProfileView.as_view(),
        name="profile",
    ),
    path(
        r"<str:username>/edit/",
        views.ProfileEditView.as_view(),
        name="profile-edit",
    ),
]
