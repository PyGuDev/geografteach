from django.shortcuts import redirect
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from django_project.response import AccessResponse
from .actions import RegistrationUserAction, ConfirmationEmailAction
from .models import User
from .serializer import CreateUserSerializer, UserSerializer


class SignUpUserAPIView(generics.CreateAPIView):
    """Регистрация пользователя"""
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        RegistrationUserAction(request).create()
        return AccessResponse()


class ConfirmUserAPIView(APIView):
    """Подтверждение пользователя"""
    permission_classes = ()

    def get(self, request):
        code = request.GET['key']
        ConfirmationEmailAction(code).confirm()
        return redirect('https://geografteach.ru/user/singin')


class SingInAPIView(TokenObtainPairView):
    """Авторизация пользователя"""
    pass


class GetUserAPIView(generics.RetrieveAPIView):
    """Вывод информации пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.request.user.id)
