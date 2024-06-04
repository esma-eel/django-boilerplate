from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from profiles.models import Profile


class JWTCreateProfilePasswordApiMixin:
    serializer = None
    receiver_field = ""
    profile_field = ""

    def get_profile(self, serializer):
        verified_field = self.profile_field + "_is_verified"
        value = serializer.validated_data.get(self.receiver_field)
        qs = Profile.objects.filter(**{self.profile_field: value, verified_field: True})
        if qs.exists():
            return qs.last()

        return None

    def get_tokens(self, user, password):
        authenticated_user = None
        if user and password:
            authenticated_user = authenticate(
                username=user.username, password=password
            )

        if authenticated_user:
            jwt_refresh_obj = RefreshToken.for_user(authenticated_user)
            return {
                "refresh": str(jwt_refresh_obj),
                "access": str(jwt_refresh_obj.access_token),
            }

        return {}

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = self.get_profile(serializer)
        password = serializer.validated_data.get("password")

        tokens = {}
        if profile:
            user = profile.user
            tokens = self.get_tokens(user, password)

        if tokens:
            return Response(tokens, status=status.HTTP_200_OK)

        return Response(
            {"message": "User not found or Password is wrong"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class JWTCreateProfileFieldOTPApiMixin(JWTCreateProfilePasswordApiMixin):
    def get_tokens(self, user, password):
        authenticated_user = user
        if authenticated_user:
            jwt_refresh_obj = RefreshToken.for_user(authenticated_user)
            return {
                "refresh": str(jwt_refresh_obj),
                "access": str(jwt_refresh_obj.access_token),
            }

        return {}
