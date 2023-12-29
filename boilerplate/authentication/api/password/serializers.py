import re

from rest_framework import serializers


class PasswordCheckSerializer(serializers.Serializer):
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def validate_password(self, value):
        password_pattern = (
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        )
        if not re.match(password_pattern, value):
            raise serializers.ValidationError(
                {
                    "password": [
                        "At least minimum 8 characters in length",
                        "At least one uppercase English letter",
                        "At least one lowercase English letter",
                        "At least one digit",
                        "At least one special character [#?!@$%^&*-]",
                    ]
                }
            )
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        repeat_password = attrs.get("repeat_password")

        if password != repeat_password:
            raise serializers.ValidationError(
                {
                    "message": (
                        "password and repeat password values, are not equal"
                    )
                }
            )

        return attrs
