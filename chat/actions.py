from django_project.exceptions import BadRequestException
from user.models import User

from .serializer import CreateMessageSerializer, ChatSerializer
from .models import MessageType, Chat, Message


class CreateChat:
    def __init__(self, data: dict, student: User):
        self._data = data
        self._student = student
        self._serializer_class = ChatSerializer

    def create(self) -> dict:
        self._check_for_exist()
        self._add_student_to_data()
        serializer = self._serialize_data()
        self._perform_create(serializer)
        return serializer.data

    def _check_for_exist(self):
        if Chat.objects.filter(student=self._student):
            raise BadRequestException(message='Chat already exist', code='already_exist')

    def _add_student_to_data(self):
        self._data['student'] = self._student.id

    def _serialize_data(self) -> ChatSerializer:
        serializer = self._serializer_class(data=self._data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def _perform_create(self, serializer):
        serializer.save()


class CreateMessage:
    def __init__(self, data: dict, user: User, chat: Chat):
        self._data = data
        self._user = user
        self._chat = chat
        self._serializer_class = CreateMessageSerializer

    def create(self) -> dict:
        self._add_chat_to_data()
        serializer = self._serialize_data()
        self._perform_create(serializer)
        return serializer.data

    def _add_chat_to_data(self):
        self._data['chat'] = self._chat.id

    def _serialize_data(self) -> CreateMessageSerializer:
        serializer = self._serializer_class(data=self._data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def _perform_create(self, serializer):
        message = serializer.save()
        message.type = MessageType.IN
        message.save()
