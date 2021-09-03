from rest_framework import serializers
from .models import Answer, ImageTask, Task


class TaskSerializer(serializers.ModelSerializer):
    """Задание"""

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'class_student',
            'description',
            'date',
        ]


class ImagesSerializer(serializers.ModelSerializer):
    """Вывод изобрадений заданий"""
    class Meta:
        model = ImageTask
        fields = '__all__'


class AddAnswerSerializer(serializers.ModelSerializer):
    """Сериалайзер добовления ответа"""
    class Meta:
        model = Answer
        fields = ('id', 'author', 'description', 'file_answer', 'task')


class AnswerSerializer(serializers.ModelSerializer):
    """Вывод полной информации ответа"""
    author = serializers.SlugRelatedField(slug_field='email', read_only=True)
    task = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Answer
        fields = '__all__'
