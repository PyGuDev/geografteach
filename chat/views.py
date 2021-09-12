from rest_framework.generics import CreateAPIView, ListAPIView

from django_project.response import AccessResponse, CreatedResponse

from .actions import CreateMessage, CreateChat
from .serializer import ChatSerializer, MessageSerializer, CreateMessageSerializer
from .models import Chat, Message


class CreateChatAPIView(CreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        response_data = CreateChat(data, self.request.user).create()
        return CreatedResponse(data=response_data)


class CreateMessageAPIView(CreateAPIView):
    serializer_class = CreateMessageSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        chat, _ = Chat.objects.get_or_create(pk=pk)
        return chat

    def create(self, request, *args, **kwargs):
        data = self.request.data.copy()
        response_data = CreateMessage(data, self.request.user, self.get_object()).create()
        return CreatedResponse(data=response_data)


class ListMessageAPIView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Message.objects.filter(chat__id=pk)
