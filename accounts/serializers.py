from rest_framework import serializers

from accounts.models import User

# from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "username",
            "first_name",
            "last_name",
            "is_superuser",
            "is_staff",
        ]

        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "is_staff": {"required": False},
            "is_superuser": {"required": False},
        }

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
