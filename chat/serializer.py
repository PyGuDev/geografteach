from rest_framework import serializers

from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'student']
        extra_kwargs = {'id': {'read_only': True}, 'student': {'required': False}}


class BaseMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        extra_kwargs = {'id': {'read_only': True}}


class MessageSerializer(BaseMessageSerializer):
    class Meta(BaseMessageSerializer.Meta):
        fields = ['id', 'text', 'type', 'chat']


class CreateMessageSerializer(BaseMessageSerializer):
    class Meta(BaseMessageSerializer.Meta):
        fields = ['id', 'text', 'chat']
