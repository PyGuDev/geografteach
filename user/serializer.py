from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User
from .service import send_mail


class CreateUserSerializer(serializers.ModelSerializer):
    """Добовление пользователя"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'class_number', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            class_number=validated_data.get('class_number'),
            password=validated_data.get('password')
        )
        Token.objects.create(user=user)
        send_mail(user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'class_number', 'email')
