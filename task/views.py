from django.http import Http404
from rest_framework import generics

from .models import Answer, Task, ImageTask
from .serializer import TaskSerializer, ImagesSerializer, AddAnswerSerializer, AnswerSerializer


class TaskListView(generics.ListAPIView):
    """Вывод списка заданий"""
    serializer_class = TaskSerializer

    def get_queryset(self):
        class_number = self.request.user.class_number
        queryset = Task.objects.get_available_tasks().filter(class_student=class_number)
        return queryset


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
