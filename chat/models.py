import uuid

from django.db import models
from user.models import User


class MessageAuthor:
    STUDENT = 'student'
    ADMIN = 'admin'


class Message(models.Model):
    AUTHOR_CHOICES = [
        (MessageAuthor.ADMIN, 'Администратор'),
        (MessageAuthor.STUDENT, 'Ученик')
    ]
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    text = models.TextField('Текст сообщения')
    author = models.CharField('Кто отправил', max_length=100, choices=AUTHOR_CHOICES)
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
