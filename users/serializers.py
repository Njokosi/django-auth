from django.conf import settings
from .models import CustomUser
from rest_framework.serializers import ModelSerializer


class CustomUserModelSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "password",
        ]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            validated_data["email"],
            validated_data["password"]
        )

        return user
