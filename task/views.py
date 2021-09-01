from rest_framework import generics

from .models import Answer, Task, ImageTask
from .serializer import TaskSerializer, ImagesSerializer, AddAnswerSerializer, AswerSerilizer


class TaskListView(generics.ListAPIView):
    """Вывод списка заданий"""
    serializer_class = TaskSerializer

    def get_queryset(self):
        class_number = self.request.user.class_number
        queryset = Task.objects.filter(avilable=True, class_student=class_number)
        return queryset


class TaskView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(avilable=True)


class TaskImagesView(generics.ListAPIView):
    """Вывод списка изображений задания"""
    serializer_class = ImagesSerializer

    def get_queryset(self):
        pk = self.request.path.split('/')[-2]
        queryset = ImageTask.objects.filter(to_task=pk)
        return queryset


class AddAswerView(generics.CreateAPIView):
    """Добовлени ответа"""
    serializer_class = AddAnswerSerializer


class AnswerView(generics.ListAPIView):
    """Вывод ответа"""
    serializer_class = AswerSerilizer

    def get_queryset(self):
        id_task = self.request.path.split('/')[-1]
        queryset = Answer.objects.filter(task=id_task)
        return queryset


class AnswerListView(generics.ListAPIView):
    """Вывод списка ответов"""
    serializer_class = AswerSerilizer

    def get_queryset(self):
        author = self.request.user
        queryset = Answer.objects.filter(author=author)
        return queryset
