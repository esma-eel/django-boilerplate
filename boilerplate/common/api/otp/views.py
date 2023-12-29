from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from boilerplate.adminstration.models import EmailTemplate, SMSTemplate
from boilerplate.common.api.general.serializers import (
    EmailSerializer,
    PhoneNumberSerializer,
)
from boilerplate.common.utils.otp_helpers import generate_otp_for_receiver
from boilerplate.communications.tasks import (
    celery_send_email,
    kavenegar_celery_send_sms,
)

from .serializers import EmailAndOTPSerializer, PhoneNumberAndOTPSerializer


# phone number
class RequestOTPWithPhoneNumberView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get("phone_number")

        otp_value = generate_otp_for_receiver(phone_number)

        if otp_value:
            headers = self.get_success_headers(request.data)
            try:
                token_data = {"token": otp_value}
                sms_template = SMSTemplate.objects.get(code="otp1")
                kavenegar_celery_send_sms.delay(
                    receptor=phone_number,
                    template=sms_template.code,
                    token_data=token_data,
                )

                return Response(
                    data={"message": f"OTP Sent to {phone_number}"},
                    status=status.HTTP_200_OK,
                    headers=headers,
                )
            except Exception:
                return Response(
                    data={"message": "There is no sms template for otp"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            data={"message": "Cant create otp, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerifyOTPWithPhoneNumberView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberAndOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(request.data)
        return Response(
            data={"message": "OTP is right"},
            status=status.HTTP_200_OK,
            headers=headers,
        )


# email
class RequestOTPWithEmailView(APIView):
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

        otp_value = generate_otp_for_receiver(email)

        if otp_value:
            headers = self.get_success_headers(request.data)
            try:
                token_data = {"token": otp_value}
                email_template = EmailTemplate.objects.get(code="otp1")
                email_content = email_template.content.format(**token_data)
                json_content = {
                    "title": email_template.name,
                    "content": email_content,
                }
                to_emails = [email]
                celery_send_email.delay(json_content, to_emails)

                return Response(
                    data={"message": f"OTP Sent to {email}"},
                    status=status.HTTP_200_OK,
                    headers=headers,
                )
            except Exception:
                return Response(
                    data={"message": "There is no email template for otp"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            data={"message": "Cant create otp, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerifyOTPWithEmailView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = EmailAndOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(request.data)
        return Response(
            data={"message": "OTP is right"},
            status=status.HTTP_200_OK,
            headers=headers,
        )
