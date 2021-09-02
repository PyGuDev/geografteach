from rest_framework import serializers
from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """Добовление пользователя"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'class_number', 'email', 'password')
        extra_kwargs = {'password': {'write_only': False}}

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            class_number=validated_data['class_number'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'class_number', 'email')
