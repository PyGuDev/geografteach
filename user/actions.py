import smtplib
from typing import Any

from rest_framework.request import Request
from django_project.exceptions import BadRequestException
from user.serializer import CreateUserSerializer
from .models import ConfirmEmail
from .service import Mail


class RegistrationUserAction:
    """Регистрация пользователя"""
    def __init__(self, request: Request):
        self._request = request

    def create(self):
        serializer = CreateUserSerializer(data=self._request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            Mail.send_mail(user)
        except smtplib.SMTPSenderRefused as e:
            print('Smtp error: {}'.format(e))


class ConfirmationEmailAction:
    """Подтверждение  email"""
    def __init__(self, code: str):
        self._code = self._validate_code(code)

    @staticmethod
    def _validate_code(code: Any) -> str:
        """Проверкак кода подтверждения"""
        if code and type(code) == str:
            return code
        else:
            raise BadRequestException(message='Code is required parameter was not passed', code='required_parameter')

    def confirm(self):
        """Метод подтверждения"""
        confirm_model = self._get_confirm_model()
        confirm_model.active = True
        self._validate_user(confirm_model)
        confirm_model.user.is_active = True
        confirm_model.user.save()
        confirm_model.save()

    def _get_confirm_model(self) -> ConfirmEmail:
        """Метод получения модели подтверждения"""
        try:
            return ConfirmEmail.objects.get(code=self._code)
        except ConfirmEmail.DoesNotExist:
            raise BadRequestException(data={"message": "the key does not exist", 'code': 'does_not_exist'})

    @staticmethod
    def _validate_user(confirm_model: ConfirmEmail):
        """Проверка подтверждаемого пользователя"""
        if confirm_model.user is None:
            raise BadRequestException(message="User does not exist", code="not_user")

        if confirm_model.user.is_active:
            raise BadRequestException(message="This user is already activated", code='is_activated')
