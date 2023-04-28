from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class RegisterSerializer(ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["phone_number", "full_name", "password1", "password2"]

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        full_name = attrs.get("full_name")
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")
        if password1 != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        user_qs = User.objects.filter(phone_number=phone_number)
        if user_qs.exists():
            raise serializers.ValidationError({"phone_number": "This phone number has already been registered."})
        if len(full_name) < 5 or full_name is None:
            raise serializers.ValidationError({"full_name": "Full name must be at least 5 characters long."})
        if len(password1) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        return attrs

    def create(self, validated_data):
        phone_number = validated_data.get("phone_number")
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password1")
        user_obj = User(
            phone_number=phone_number,
            username=username,
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data
