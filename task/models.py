from django.db import models
from user.models import User


class Task(models.Model):
    CLASS_NUMBERS = (
        ('5', '5 класс'),
        ('6', '6 класс'),
        ('7', '7 класс'),
        ('8', '8 класс'),
        ('9', '9 класс'),
        ('10', '10 класс'),
        ('11', '11 класс'),
    )
    title = models.CharField('Название', max_length=255)
    class_student = models.CharField('Класс', max_length=15, choices=CLASS_NUMBERS)
    description = models.TextField('Описание')
    date = models.DateTimeField('Дата сдачи')
    avilable = models.BooleanField('Автивно', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задние'
        verbose_name_plural = 'Задания'


class Answer(models.Model):
    ESTIMATION = (
        ('2', 'Не удовлетворительно'),
        ('3', 'Удовлетворительно'),
        ('4', 'Хорошо'),
        ('5', 'Отлично'),
    )

    author = models.ForeignKey(User, verbose_name='Автор ответа', on_delete=models.CASCADE)
    description = models.TextField('Описание ответа')
    file_answer = models.FileField('Файл ответа', blank=True)
    task = models.ForeignKey(Task, verbose_name='Задание', on_delete=models.CASCADE)
    estimation = models.CharField('Оценка', max_length=24, choices=ESTIMATION, blank=True)
    commets_answer = models.TextField('Комментарий к ответу', blank=True)

    def __str__(self):
        return self.id.__str__() + '_' + self.author.first_name + '_' + self.author.last_name

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class ImageTask(models.Model):
    img = models.ImageField('Изображение', upload_to='uploads/task/images')
    to_task = models.ForeignKey(Task, verbose_name='Изображение', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.img.path

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'




