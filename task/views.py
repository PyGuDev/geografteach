from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import generics, views
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from .models import Answer, Task, ImageTask, TestTask, TestQuestion, TestSession, UserAnswerForQuestion, \
    PossibleQuestionAnswer
from .serializer import TaskSerializer, ImagesSerializer, AddAnswerSerializer, AnswerSerializer, TestTaskSerializer, \
    ListTestTaskSerializer, ListTestQuestionSerializer, UserAnswerForQuestionSerializer, TestResultSerializer, \
    TestResultSerializerForListTest, AnswerSerializerByListTask


class TaskListView(generics.ListAPIView):
    """Вывод списка заданий"""
    serializer_class = TaskSerializer

    def get_queryset(self):
        class_number = self.request.user.class_number
        queryset = Task.objects.get_available_tasks().filter(class_student=class_number)
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data.copy()

        new_data = []
        for item in data:
            id = item.get('id')
            task = self.get_queryset().get(pk=id)
            new_item = item
            try:
                answer = task.answers.get(author=self.request.user)
                new_item['answer'] = AnswerSerializerByListTask(instance=answer).data
            except Answer.DoesNotExist:
                new_item['answer'] = None

            new_data.append(new_item)

        response.data = new_data
        return response


class TaskView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.get_tasks_by_class_number(self.request.user.class_number)

    def get_object(self):
        pk = self.kwargs.get('task_pk')
        return self.get_queryset().get(pk=pk)


class TaskImagesView(generics.ListAPIView):
    """Вывод списка изображений задания"""
    serializer_class = ImagesSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        queryset = ImageTask.objects.filter(to_task=pk)
        return queryset


class AddAnswerView(generics.CreateAPIView):
    """Добовлени ответа"""
    serializer_class = AddAnswerSerializer


class AnswerView(generics.RetrieveAPIView):
    """Вывод ответа"""
    serializer_class = AnswerSerializer

    def get_queryset(self):
        return Answer.objects.all()

    def get_object(self):
        user = self.request.user
        task_pk = self.kwargs.get('task_pk')
        try:
            answer = self.get_queryset().get(task_id=task_pk, author_id=user.id)
        except Answer.DoesNotExist:
            raise Http404
        return answer


class AnswerListView(generics.ListAPIView):
    """Вывод списка ответов"""
    serializer_class = AnswerSerializer

    def get_queryset(self):
        author = self.request.user
        queryset = Answer.objects.filter(author=author)
        return queryset


class ListTestView(generics.ListAPIView):
    serializer_class = ListTestTaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return TestTask.objects.filter()
        return TestTask.objects.filter(class_student=user.class_number, enabled=True)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data.copy()

        new_data = []
        for item in data:
            uid = item.get('uid')
            test = self.get_queryset().get(uid=uid)
            new_item = item
            try:
                session = test.test_sessions.get(user=self.request.user)
                new_item['result'] = TestResultSerializerForListTest(instance=session).data
            except TestSession.DoesNotExist:
                new_item['result'] = None
            new_data.append(new_item)

        response.data = new_data
        return response


class BaseTestMixin:
    def get_test(self):
        test_pk = self.kwargs.get('test_pk')
        try:
            obj = TestTask.objects.get(pk=test_pk)
        except TestQuestion.DoesNotExist:
            raise Http404
        return obj


class TestView(BaseTestMixin, generics.ListAPIView):
    serializer_class = ListTestQuestionSerializer

    def get_queryset(self):
        user = self.request.user
        test = self.get_test()
        if user.is_admin:
            return TestQuestion.objects.filter(test__enabled=True, test=test)
        return TestQuestion.objects.filter(test__class_student=user.class_number, test=test)

    def list(self, request, *args, **kwargs):
        session = self.get_test_session()
        if session.end_time or session.test.duration_session + session.start_time < timezone.now():
            if session.end_time is None:
                session.end_time = timezone.now()
                session.result = 0
                session.save()
            return redirect('result_test', test_pk=session.test.pk, session_pk=session.pk)

        return super().list(request, *args, **kwargs)

    def get_test_session(self) -> TestSession:
        session_pk = self.kwargs.get('session_pk')
        try:
            return self.request.user.test_sessions.get(pk=session_pk)
        except TestSession.DoesNotExist:
            raise Http404


class TestExpireTime(views.APIView):
    def get(self, request, *args, **kwargs):
        session_pk = self.kwargs.get('session_pk')
        try:
            session = TestSession.objects.get(pk=session_pk)
        except TestSession.DoesNotExist:
            return Response({'error': 'test session not found'}, status=400)
        expired_at = (session.test.duration_session + session.start_time).timestamp()
        return Response({'expired_at': expired_at}, status=200)


class CreateTestSessionView(BaseTestMixin, views.APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        test = self.get_test()
        session, _ = TestSession.objects.get_or_create(test=test, user=user)
        return redirect('detail_test', test_pk=test.pk, session_pk=session.pk)


class CreateTestResultView(generics.GenericAPIView):
    serializer_class = UserAnswerForQuestionSerializer
    queryset = UserAnswerForQuestion.objects.all()

    def get_serializers(self, *args, **kwargs):
        return super().get_serializer(many=True, *args, *kwargs)

    def get_test_session(self):
        session_pk = self.kwargs.get('session_pk')
        try:
            session = self.request.user.test_sessions.get(pk=session_pk)
            return session
        except TestSession.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        session = self.get_test_session()
        if session.end_time is None:
            raise Http404
        serializer = TestResultSerializer(instance=session)
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        session = self.get_test_session()

        if session.end_time:
            return redirect('result_test', test_pk=session.test.pk, session_pk=session.pk)

        raw_data = self.request.data
        serializer = self.serializer_class(many=True, data=raw_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        self.validate_answers(data)
        count_current_answer = 0
        for item in data:
            answer = UserAnswerForQuestion(
                question_id=item.get('question'),
                answer_id=item.get('answer'),
                session=session
            )
            count_current_answer += answer.answer.is_current
            answer.save()

        session.end_time = timezone.now()
        session.result = (100 / session.test.questions.count()) * count_current_answer
        session.save()
        return redirect('result_test', test_pk=session.test.pk, session_pk=session.pk)

    def validate_answers(self, data: list):
        custom_exception = APIException
        custom_exception.status_code = 400

        for item in data:
            question_id = item.get('question')
            answer_id = item.get('answer')
            try:
                question = TestQuestion.objects.get(pk=question_id)
                answer = PossibleQuestionAnswer.objects.get(id=answer_id)
                if answer.question != question:
                    custom_exception.default_detail = {
                        'msg': f'Answer id={answer.pk} not equal question id={question.pk}'
                    }
                    raise custom_exception

            except ObjectDoesNotExist as exc:
                print(exc)
                custom_exception.default_detail = {
                    'msg': f'Invalid answer_id={answer_id} or question_id={question_id}'
                }
                raise custom_exception

            except TypeError as exc:
                print(exc)
                custom_exception.default_detail = {
                    'msg': f'Invalid answer_id={answer_id} or question_id={question_id}'
                }
                raise custom_exception


class TestSessionView(generics.CreateAPIView):
    """Cессия теста"""
    pass