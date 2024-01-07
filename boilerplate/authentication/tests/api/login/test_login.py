from django.urls import reverse
from rest_framework import status

# from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from boilerplate.common.tests.test_mixins import UserAPITestCase
from boilerplate.common.utils.otp_helpers import (
    generate_otp_for_receiver,
    # get_otp_of_receiver,
)

User = get_user_model()


class JWTAPITestCase(UserAPITestCase):
    def test_jwt_create(self):
        url = reverse("api-authentication:jwt-create")

        data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_create_wrong_password(self):
        url = reverse("api-authentication:jwt-create")

        data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("strong_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_jwt_create_phone(self):
        url = reverse("api-authentication:jwt-create-phone")

        data = {
            "phone_number": self.user_data.get("phone_number"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_create_phone_otp(self):
        url = reverse("api-authentication:jwt-create-phone-otp")
        receiver = self.user_data.get("phone_number")

        requested_otp = generate_otp_for_receiver(receiver)
        self.assertIsNotNone(requested_otp, "Could'nt generate otp")

        data = {
            "receiver": receiver,
            "otp": requested_otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_create_email(self):
        url = reverse("api-authentication:jwt-create-email")

        data = {
            "email": self.user_data.get("email"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_create_email_otp(self):
        url = reverse("api-authentication:jwt-create-email-otp")
        receiver = self.user_data.get("email")

        requested_otp = generate_otp_for_receiver(receiver)
        self.assertIsNotNone(requested_otp, "Could'nt generate otp")

        data = {
            "receiver": receiver,
            "otp": requested_otp,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_jwt_refresh(self):
        login_url = reverse("api-authentication:jwt-create")
        refresh_url = reverse("api-authentication:jwt-refresh")

        login_data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        refresh_token = response_data.get("refresh")
        refresh_data = {
            "refresh": refresh_token,
        }

        response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TokenAPITestCase(UserAPITestCase):
    def test_token_create(self):
        url = reverse("api-authentication:token-create")

        data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_refresh(self):
        login_url = reverse("api-authentication:token-create")
        refresh_url = reverse("api-authentication:token-refresh")

        login_data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        token = response_data.get("token")
        refresh_data = {
            "token": token,
        }

        response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_verify(self):
        login_url = reverse("api-authentication:token-create")
        verify_url = reverse("api-authentication:token-verify")

        login_data = {
            "username": self.user_data.get("username"),
            "password": self.user_data.get("weak_password"),
        }

        response = self.client.post(login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        token = response_data.get("token")
        verify_data = {
            "token": token,
        }

        response = self.client.post(verify_url, verify_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
