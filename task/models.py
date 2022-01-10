import uuid

from django.db import models

from user.models import User


class TaskManager(models.Manager):
    def get_available_tasks(self):
        return self.get_queryset().filter(available=True)

    def get_tasks_by_class_number(self, class_number: int):
        return self.get_available_tasks().filter(class_student=class_number)


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
    available = models.BooleanField('Автивно', default=True)

    objects = TaskManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задние'
        verbose_name_plural = 'Задания'
        db_table = 'task'


class Answer(models.Model):
    ESTIMATION = (
        ('2', 'Не удовлетворительно'),
        ('3', 'Удовлетворительно'),
        ('4', 'Хорошо'),
        ('5', 'Отлично'),
    )

    author = models.ForeignKey(User, verbose_name='Автор ответа', on_delete=models.CASCADE)
    description = models.TextField('Описание ответа', blank=True)
    file_answer = models.FileField('Файл ответа', blank=True)
    task = models.ForeignKey(Task, verbose_name='Задание', related_name='answers', on_delete=models.CASCADE)
    estimation = models.CharField('Оценка', max_length=24, choices=ESTIMATION, blank=True)
    comments_answer = models.TextField('Комментарий к ответу', blank=True)

    def __str__(self):
        return self.id.__str__() + '_' + self.author.first_name + '_' + self.author.last_name

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        db_table = 'answer'


class ImageTask(models.Model):
    img = models.ImageField('Изображение', upload_to='uploads/task/images')
    to_task = models.ForeignKey(Task, verbose_name='Изображение', on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.img.path

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        db_table = 'image_for_task'


class TestTask(models.Model):
    uid = models.CharField(max_length=36, primary_key=True, default=uuid.uuid4)
    title = models.CharField('Название', max_length=300)
    duration_session = models.DurationField('Время на прохождение')
    expiry_date = models.DateTimeField('Дата окончания действия', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        db_table = 'test'


class TestQuestion(models.Model):
    question = models.TextField('Текст вопроса')
    image = models.ImageField('Изображение для вопроса', blank=True)
    test = models.ForeignKey('TestTask', on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return f'{self.question}'

    class Meta:
        verbose_name = 'Вопросы к тесту'
        verbose_name_plural = 'Вопросы к тесту'
        db_table = 'question'


class PossibleQuestionAnswer(models.Model):
    answer = models.TextField('Ответ на вопрос')
    question = models.ForeignKey('TestQuestion', on_delete=models.CASCADE, related_name='answers')
    is_current = models.BooleanField('Правильный?', blank=True, default=False)

    def __str__(self):
        return f'Вопрос: {self.question} ответ: {self.answer}'

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        db_table = 'possible_answer'


class TestSession(models.Model):
    test = models.ForeignKey('TestTask', on_delete=models.CASCADE, related_name='test_sessions')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    start_time = models.DateTimeField('Время начала')
    end_time = models.DateTimeField('Время завершения')
    result = models.DecimalField('Результат в процентах', decimal_places=1, max_digits=4, blank=True)

    def __str__(self):
        return f'Тест: {self.test} пользователь: {self.user}'

    class Meta:
        verbose_name = 'Тест ученика'
        verbose_name_plural = 'Тесты учеников'
        db_table = 'test_session'


class UserAnswerForQuestion(models.Model):
    answer = models.ForeignKey('PossibleQuestionAnswer', on_delete=models.CASCADE, related_name='user_answer')
    question = models.ForeignKey('TestQuestion', on_delete=models.CASCADE, related_name='user_answer')
    session = models.ForeignKey('TestSession', on_delete=models.CASCADE, related_name='user_answer')

    def __str__(self):
        return f"{self.session} {self.question} {self.answer}"

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'
        db_table = 'user_answer'
