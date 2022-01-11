from rest_framework import serializers
from .models import Answer, ImageTask, Task, TestTask, TestQuestion, TestSession, PossibleQuestionAnswer,\
    UserAnswerForQuestion


class TaskSerializer(serializers.ModelSerializer):
    """Задание"""
    date = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

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


class ListTestTaskSerializer(serializers.ModelSerializer):
    """Сериализатор списка вывода тестов"""
    class Meta:
        model = TestTask
        exclude = ['enabled', 'class_student']


class TestTaskSerializer(serializers.ModelSerializer):
    """Сериализатор вывода тестов"""
    class Meta:
        model = TestTask
        exclude = ['enabled', 'class_student']


class TestTaskSessionSerializer(serializers.ModelSerializer):
    """Сериализатор сессии тестов"""
    class Meta:
        model = TestSession
        fields = '__all__'


class PossibleQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PossibleQuestionAnswer
        fields = ['id', 'answer']


class ListTestQuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField('get_answers')

    def get_answers(self, obj):
        answers = obj.answers.all()
        return PossibleQuestionAnswerSerializer(instance=answers, many=True).data

    class Meta:
        model = TestQuestion
        exclude = ['test']


class TestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestQuestion
        fields = ['id']


class AnswerForQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PossibleQuestionAnswer
        fields = ['id']


class UserAnswerForQuestionSerializer(serializers.Serializer):
    question = serializers.IntegerField(required=True)
    answer = serializers.IntegerField(required=True)


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSession
        fields = '__all__'

