from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

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
        fields = ('id', 'first_name', 'last_name', 'class_number', 'email')


class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = self.user.email
        refresh = self.get_token(self.user)
        data['token_expire'] = refresh['exp']
        print(data)
        return data


class RefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = RefreshToken(attrs['refresh'])
        data['token_expire'] = refresh['exp']
        return data
