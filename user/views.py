from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from django_project.response import AccessResponse, BadResponse

from .actions import RegistrationUser
from .models import User, ConfirmEmail
from .serializer import CreateUserSerializer, UserSerializer


class SignUpUser(generics.CreateAPIView):
    """Регистрация пользователя"""
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        RegistrationUser(request).create()

        return AccessResponse()


class ConfirmUser(APIView):
    """Подтверждение пользователя"""
    permission_classes = ()

    def get(self, requset):
        code = requset.GET['key']
        try:
            conf_email = ConfirmEmail.objects.get(code=code)
            conf_email.active = True
        except:
            return Response(status=400, data={"error": "the key does not exist"})

        try:
            user = User.objects.get(email=conf_email.user)
        except:
            return Response(status=400, data={"error": "user does not exist"})

        if user.is_active == True:
            return Response(status=200, data={"warning": "This user is already activated"})
        else:
            user.is_active = True
        user.save()
        conf_email.save()
        return redirect('http://geografteach.ru/user/singin')


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
