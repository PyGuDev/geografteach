from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from django_project.response import AccessResponse

from .actions import RegistrationUserAction, ConfirmationEmailAction
from .models import User
from .serializer import CreateUserSerializer, UserSerializer


class SignUpUser(generics.CreateAPIView):
    """Регистрация пользователя"""
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        RegistrationUserAction(request).create()
        return AccessResponse()


class ConfirmUser(APIView):
    """Подтверждение пользователя"""
    permission_classes = ()

    def get(self, request):
        code = request.GET['key']
        ConfirmationEmailAction(code).confirm()
        return redirect('https://geografteach.ru/user/singin')


class SingIn(TokenObtainPairView):
    """Авторизация пользователя"""
    pass


class Logout(APIView):
    """Выход из аккаунта"""

    def get(self, request):
        try:
            logout(request)
            return Response(status=200)
        except:
            return Response(status=400)


class GetUser(generics.RetrieveAPIView):
    """Вывод информации пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
