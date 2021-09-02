from rest_framework.request import Request

from user.serializer import CreateUserSerializer
from .service import SendConfirmMail


class RegistrationUser:
    def __init__(self, request: Request):
        self._request = request

    def create(self):
        serializer = CreateUserSerializer(data=self._request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        SendConfirmMail.send_mail(user)


