from rest_framework.request import Request

from user.serializer import CreateUserSerializer


class RegistrationUser:
    def __init__(self, serializer_class: CreateUserSerializer, request: Request):
        self._serializer = serializer_class
        self._request = request

    def create(self):
        pass
