import copy
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db import transaction
from profiles.api.serializers import ProfileModelSerializer
from .serializers import (
    CreateUserModelSerializer,
    UserModelSerializer,
    RegisterUserModelSerializer,
    RegisterUserSerilaizer,
)

User = get_user_model()


class UserCreateAPIView(APIView):
    serializer_class = CreateUserModelSerializer
    response_serializer_class = UserModelSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def profile_update(self, user_object, profile_data):
        profile_object = user_object.profile
        serializer = ProfileModelSerializer(
            instance=profile_object, data=profile_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        profile_object = serializer.save()
        return profile_object

    def authentication_set(self, user_object, authenticate_data):
        password = authenticate_data.get("password")
        user_object.set_password(password)
        user_object.save()
        return user_object

    def user_create(self, user_data):
        profile_data = user_data.pop("profile")
        user_object = User.objects.create(**user_data)
        self.profile_update(user_object, profile_data)
        return user_object

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = copy.deepcopy(serializer.data)
        user_data = serializer_data.pop("user")
        authentication_data = serializer_data.pop("authentication")

        user_object = self.user_create(user_data)
        self.authentication_set(user_object, authentication_data)

        created_serializer = self.response_serializer_class(instance=user_object)

        return Response(
            created_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class UserRegisterAPIView(UserCreateAPIView):
    serializer_class = RegisterUserSerilaizer
    response_serializer_class = RegisterUserModelSerializer
    allowed_methods = ["post"]
    http_method_names = ["post"]

    permission_classes = []
    authentication_classes = []