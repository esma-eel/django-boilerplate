# from django.urls import reverse
# from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            "name": "Test User",
            "username": "test_user",
            "email": "test_email@test.com",
            "phone_number": "09121234579",
            "weak_password": "test_password",
            "strong_password": "W34el@come",
            "city": "Karaj",
            "address": "just address",
        }
        self.user = User.objects.create(
            username=self.user_data.get("username"),
        )
        self.user.set_password(self.user_data.get("weak_password"))
        self.user.save()
        self.user_profile = self.user.profile

    def tearDown(self):
        # just for more information
        self.user_profile.delete()
        self.user.delete()

        return super().tearDown()
