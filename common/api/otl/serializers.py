from rest_framework import serializers
from common.utils.otl_helpers import verify_input_otl_of_receiver
from profiles.models import Profile

class EmailAndOTLSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otl = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        otl = attrs.get("otl")

        qs = Profile.objects.filter(email=email)
        if not qs.exists():
            raise serializers.ValidationError({"email": "Wrong email!"})

        result = verify_input_otl_of_receiver(otl, email)

        if not result:
            raise serializers.ValidationError(
                {"otl": "OTL Token is wrong or expired"}
            )

        return attrs
