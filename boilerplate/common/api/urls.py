from django.urls import path
from .otp import views as otp_views


app_name = "api-common"

otp_urlpatterns = [
    # otp
    path(
        "otp/sms/create/",
        otp_views.RequestOTPWithPhoneNumberView.as_view(),
        name="otp-sms-create",
    ),
    path(
        "otp/sms/verify/",
        otp_views.VerifyOTPWithPhoneNumberView.as_view(),
        name="otp-sms-verify",
    ),
    path(
        "otp/email/create/",
        otp_views.RequestOTPWithEmailView.as_view(),
        name="otp-email-create",
    ),
    path(
        "otp/email/verify/",
        otp_views.VerifyOTPWithEmailView.as_view(),
        name="otp-email-verify",
    ),
]

urlpatterns = [] + otp_urlpatterns
