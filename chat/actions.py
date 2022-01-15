from django_project.exceptions import BadRequestException
from user.models import User

from .serializer import CreateMessageSerializer, ChatSerializer
from .models import MessageType, Chat, Message


class CreateMessage:
    def __init__(self, data: dict, user: User):
        self._data = data
        self._user = user
        self._serializer_class = CreateMessageSerializer

    def create(self) -> dict:
        if not self._user.is_admin:
            chat, _ = Chat.objects.get_or_create(student=self._user)
        self._add_chat_to_data(chat)
        serializer = self._serialize_data()
        self._perform_create(serializer)
        return serializer.data

    def _add_chat_to_data(self, chat):
        self._data['chat'] = chat.id

    def _serialize_data(self) -> CreateMessageSerializer:
        serializer = self._serializer_class(data=self._data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def _perform_create(self, serializer):
        message = serializer.save()
        if self._user.is_admin:
            message.type = MessageType.OUT
        else:
            message.type = MessageType.IN
        message.save()
