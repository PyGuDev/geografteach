import uuid

from django.db import models
from user.models import User


class MessageType:
    IN = 'incoming'
    OUT = 'outgoing'


class Message(models.Model):
    TYPE_MESSAGE_CHOICES = [
        (MessageType.OUT, 'Исходящие'),
        (MessageType.IN, 'Входящие')
    ]
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField('Текст сообщения')
    type = models.CharField('Тип сообщения', max_length=100, choices=TYPE_MESSAGE_CHOICES)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='message', verbose_name='Чат')

    def __str__(self):
        return 'Сообщение {}'.format(self.id)

    class Meta:
        verbose_name = 'Собщение'
        verbose_name_plural = 'Собщения'


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='chat', verbose_name='Ученик')

    def __str__(self):
        return 'Чат с {}'.format(self.student)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
