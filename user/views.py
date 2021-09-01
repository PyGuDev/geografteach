from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from .serializer import CreateUserSerializer, UserSerializer
from .models import User, ConfirmEmail


class SingupUser(generics.CreateAPIView):
    """Регистрация пользователя"""
    serializer_class = CreateUserSerializer
    authentication_classes = ()
    permission_classes = ()

    def perform_create(self, serializer):
        serializer.save()


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
            return Response(status=202, data={"warning": "This user is already activated"})
        else:
            user.is_active = True
        user.save()
        conf_email.save()
        return redirect('http://geografteach.ru/user/singin')


class SingIn(APIView):
    """Авторизация пользователя"""
    http_method_names = ['post']
    permission_classes = ()

    def post(self, requset):
        email = requset.data["email"]
        password = requset.data['password']
        user = authenticate(requset, username=email, password=password)
        if user is not None:
            login(requset, user)
            if user.is_admin:
                return Response({"token": user.auth_token.key, "user": user.email, "id": user.id, "admin": True})
            else:
                return Response({"token": user.auth_token.key, "user": user.email, "id": user.id, "admin": False})
        else:
            return Response({"error": "Wrong Credentials"}, status=400)


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

