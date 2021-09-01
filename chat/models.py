from django.db import models
from user.models import User


class MessageUser(models.Model):
    text = models.TextField('Текст сообщения')
    author = models.ForeignKey(User, verbose_name='Отправитель', on_delete=models.CASCADE)

    def __str__(self):
        return self.author.email + '_' + self.id.__str__()

    class Meta:
        verbose_name = 'Собщение'
        verbose_name_plural = 'Собщения'


class MessageAdmin(models.Model):
    text = models.TextField('Текст сообщения')
    to_message = models.ForeignKey(MessageUser, verbose_name='Кому', on_delete=models.CASCADE)

    def __str__(self):
        return  'admin_to_' + self.to_message.author.email + '_' + self.id.__str__()

    class Meta:
        verbose_name = 'Собщение пользователям'
        verbose_name_plural = 'Собщения пользователям'