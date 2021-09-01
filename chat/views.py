from rest_framework import generics

from .models import MessageAdmin, MessageUser
from .serializer import MessagesToAdminSerializer, MessagesToUserSerializer


class CreateMessageView(generics.CreateAPIView):
    serializer_class = MessagesToAdminSerializer


class ListMessageToAdmin(generics.ListAPIView):
    serializer_class = MessagesToAdminSerializer

    def get_queryset(self):
        if self.request.user.is_admin:
            queryset = MessageUser.objects.all()
        else:
            queryset = MessageUser.objects.filter(author=self.request.user)
        return queryset


class ListMessageToUser(generics.ListAPIView):
    serializer_class = MessagesToUserSerializer

    def get_queryset(self):
        queryset = MessageAdmin.objects.filter(to_message__author=self.request.user)
        return queryset
