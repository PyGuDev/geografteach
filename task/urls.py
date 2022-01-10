from django.urls import path
from .views import TaskListView, TaskView, TaskImagesView, AddAnswerView, AnswerListView, AnswerView

urlpatterns = [
    path('task/', TaskListView.as_view()),
    path('task/<int:task_pk>/', TaskView.as_view()),
    path('task/<int:task_pk>/answer/', AnswerView.as_view()),
    path('task/image/<int:pk>/', TaskImagesView.as_view()),
    path('task/answer/add/', AddAnswerView.as_view()),

    # path('task/<int:task_pk>/answer/<int:answer_pk>', AnswerView.as_view())
]