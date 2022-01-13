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
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerSerializerByListTask(serializers.ModelSerializer):
    """Вывод полной информации ответа"""
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = Answer
        fields = ['estimation', 'created_at', ]


class FormattingDurationMixin:
    def formatting_duration(self, obj):
        if obj.duration_session:
            raw_duration_session = str(obj.duration_session).split(' ')
            if len(raw_duration_session) > 1:
                day = f'{raw_duration_session[0]} д'
            else:
                day = None
            raw_time = raw_duration_session[-1].split(':')

            hour = f'{int(raw_time[0])} час' if int(raw_time[0]) >= 1 else None
            minute = f'{int(raw_time[1])} мин' if int(raw_time[1]) >= 1 else None
            second = f'{int(raw_time[2])} сек' if int(raw_time[2]) >= 1 else None
            duration = [day, hour, minute, second]
            duration = ' '.join(list(filter(lambda x: True if x else False, duration)))
            return duration
        return None


class ListTestTaskSerializer(serializers.ModelSerializer, FormattingDurationMixin):
    """Сериализатор списка вывода тестов"""
    expiry_date = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    duration_session = serializers.SerializerMethodField('formatting_duration')

    class Meta:
        model = TestTask
        exclude = ['enabled', 'class_student']


class TestTaskSerializer(serializers.ModelSerializer, FormattingDurationMixin):
    """Сериализатор вывода тестов"""
    duration_session = serializers.SerializerMethodField('formatting_duration')

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
    test = TestTaskSerializer()
    start_time = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    end_time = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = TestSession
        fields = '__all__'


class TestResultSerializerForListTest(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    end_time = serializers.DateTimeField(format="%d.%m.%Y %H:%M")

    class Meta:
        model = TestSession
        exclude = ['test']

