from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from boilerplate.adminstration.models import EmailTemplate
from boilerplate.common.api.otl.serializers import EmailAndOTLSerializer
from boilerplate.common.api.otp.serializers import PhoneNumberAndOTPSerializer
from boilerplate.common.api.general.serializers import EmailSerializer
from boilerplate.common.utils.otl_helpers import generate_otl_for_receiver
from boilerplate.communications.tasks import celery_send_email
from boilerplate.profiles.models import ProfileEmail, ProfilePhoneNumber

from .serializers import PasswordCheckSerializer


class ResetPasswordOTPWithPhoneNumberView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        password_serializer = PasswordCheckSerializer(data=request.data)
        password_serializer.is_valid(raise_exception=True)
        phone_number_otp_serializer = PhoneNumberAndOTPSerializer(
            data=request.data
        )
        phone_number_otp_serializer.is_valid(raise_exception=True)

        phone_number = phone_number_otp_serializer.validated_data.get(
            "phone_number"
        )

        qs_phone_numbers_objects = ProfilePhoneNumber.objects.filter(
            is_primary=True, number=phone_number, is_verified=True
        )
        if not qs_phone_numbers_objects.exists():
            return Response(
                {
                    "phone_number": (
                        "Please enter your verified primary phone number"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        phone_number_object = qs_phone_numbers_objects.last()
        profile_user_obj = phone_number_object.profile.user

        password_value = password_serializer.validated_data.get("password")
        profile_user_obj.set_password(password_value)
        profile_user_obj.save()

        headers = self.get_success_headers(request.data)
        return Response(
            data={
                "message": (
                    f"Password reset for user '{profile_user_obj}' was"
                    " successful"
                )
            },
            status=status.HTTP_200_OK,
            headers=headers,
        )


class ResetPasswordRequestOTLWithEmailView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")

        otl_value = generate_otl_for_receiver(email)

        if otl_value:
            headers = self.get_success_headers(request.data)
            link = reverse(
                "authentication:reset-password-email-otl",
                args=[otl_value],
                request=request,
            )
            try:
                token_data = {"link": link}
                email_template = EmailTemplate.objects.get(code="otl1")
                email_content = email_template.content.format(**token_data)
                json_content = {
                    "title": email_template.name,
                    "content": email_content,
                }
                to_emails = [email]
                celery_send_email.delay(json_content, to_emails)

                return Response(
                    data={"message": f"Link Sent to {email}"},
                    status=status.HTTP_200_OK,
                    headers=headers,
                )
            except Exception:
                return Response(
                    data={
                        "message": (
                            "There is no email template for otl reset passsword"
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            data={"message": "Cant create OTL for reset password, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ResetPasswordOTLWithEmailView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        password_serializer = PasswordCheckSerializer(data=request.data)
        password_serializer.is_valid(raise_exception=True)
        email_otl_serializer = EmailAndOTLSerializer(data=request.data)
        email_otl_serializer.is_valid(raise_exception=True)

        email = email_otl_serializer.validated_data.get("email")

        qs_email_objects = ProfileEmail.objects.filter(
            is_primary=True, email=email, is_verified=True
        )
        if not qs_email_objects.exists():
            return Response(
                {"email": "Please enter your verified primary email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email_object = qs_email_objects.last()
        profile_user_obj = email_object.profile.user

        password_value = password_serializer.validated_data.get("password")
        profile_user_obj.set_password(password_value)
        profile_user_obj.save()

        headers = self.get_success_headers(request.data)
        return Response(
            data={
                "message": (
                    f"Password reset for user '{profile_user_obj}' was"
                    " successful"
                )
            },
            status=status.HTTP_200_OK,
            headers=headers,
        )


class AuthenticatedUserChangePassword(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        password_serializer = PasswordCheckSerializer(data=request.data)
        password_serializer.is_valid(raise_exception=True)
        user_obj = request.user

        password_value = password_serializer.validated_data.get("password")
        user_obj.set_password(password_value)
        user_obj.save()

        headers = self.get_success_headers(request.data)
        return Response(
            data={
                "message": (
                    f"Password change for user '{user_obj}' was successful"
                )
            },
            status=status.HTTP_200_OK,
            headers=headers,
        )
