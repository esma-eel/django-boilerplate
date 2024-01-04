from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from boilerplate.common.api.otp.serializers import (
    EmailOTPSerializer,
    PhoneOTPSerializer,
)
from boilerplate.profiles.models import ProfileEmail, ProfilePhoneNumber

from .serializers import (
    EmailPasswordSerializer,
    PhonePasswordSerializer,
)


class JWTCreateProfileFieldPassword(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    serializer = None
    profile_model = None
    profile_field = ""

    def validate_serializer(self, request):
        self.validated_serializer = self.serializer(data=request.data)
        self.validated_serializer.is_valid(raise_exception=True)
        return self.validated_serializer

    def get_password(self):
        return self.validated_serializer.validated_data.get("password")

    def get_profile_field(self):
        return self.validated_serializer.validated_data.get(self.profile_field)

    def get_queryset(self):
        field_value = self.get_profile_field()
        queryset = self.profile_model.objects.filter(
            is_primary=True,
            is_verified=True,
            **{self.profile_field: field_value},
        )

        return queryset

    def get_profile_object(self):
        queryset = self.get_queryset()
        if not queryset.exists():
            return None

        profile = queryset.last().profile
        return profile

    def get_profile_user(self):
        profile_object = self.get_profile_object()
        if profile_object:
            profile_user = profile_object.user
            return profile_user

        return None

    def authenticate_user(self):
        password = self.get_password()
        user = self.get_profile_user()

        if user and password:
            authenticated_user = authenticate(
                username=user.username, password=password
            )
            return authenticated_user

        return None

    def get_tokens(self):
        authenticated_user = self.authenticate_user()
        if authenticated_user:
            jwt_refresh_obj = RefreshToken.for_user(authenticated_user)
            return {
                "refresh": str(jwt_refresh_obj),
                "access": str(jwt_refresh_obj.access_token),
            }

        return {}

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        self.validate_serializer(request)
        headers = self.get_success_headers(self.validated_serializer.data)
        tokens = self.get_tokens()
        if tokens:
            return Response(tokens, status=status.HTTP_200_OK, headers=headers)

        return Response(
            {"message": f"{self.profile_field.title()} or password is wrong"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class JWTCreateWithPhoneNumberAndPassword(JWTCreateProfileFieldPassword):
    serializer = PhonePasswordSerializer
    profile_model = ProfilePhoneNumber
    profile_field = "phone_number"


class JWTCreateWithEmailAndPassword(JWTCreateProfileFieldPassword):
    serializer = EmailPasswordSerializer
    profile_model = ProfileEmail
    profile_field = "email"


class JWTCreateProfileFieldOTP(JWTCreateProfileFieldPassword):
    serializer_field = ""

    def get_password(self):
        return None

    def get_profile_field(self):
        return self.validated_serializer.validated_data.get(
            self.serializer_field
        )

    def get_tokens(self):
        authenticated_user = self.get_profile_user()
        if authenticated_user:
            jwt_refresh_obj = RefreshToken.for_user(authenticated_user)
            return {
                "refresh": str(jwt_refresh_obj),
                "access": str(jwt_refresh_obj.access_token),
            }

        return {}


class JWTCreateWithPhoneNumberAndOTPView(JWTCreateProfileFieldOTP, APIView):
    serializer = PhoneOTPSerializer
    serializer_field = "receiver"
    profile_model = ProfilePhoneNumber
    profile_field = "phone_number"


class JWTCreateWithEmailAndOTPView(JWTCreateProfileFieldOTP, APIView):
    serializer = EmailOTPSerializer
    serializer_field = "receiver"
    profile_model = ProfileEmail
    profile_field = "email"
