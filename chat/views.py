from rest_framework.generics import CreateAPIView, ListAPIView

from django_project.response import AccessResponse, CreatedResponse

from .actions import CreateMessage
from .serializer import MessageSerializer, CreateMessageSerializer
from .models import Chat, Message


class CreateMessageAPIView(CreateAPIView):
    serializer_class = CreateMessageSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data.copy()
        response_data = CreateMessage(data, self.request.user).create()
        return CreatedResponse(data=response_data)


class ListMessageAPIView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        pk = self.request.user.chat.last().pk
        return Message.objects.filter(chat__id=pk)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if self.request.user.is_admin:
            data = response.data
            new_data = []
            for item in data:
                new_item = item
                new_item.type = 'outcoming' if item.type == 'incoming' else 'incoming'
                new_data.append(new_item)

            response.data = new_data

        return response
