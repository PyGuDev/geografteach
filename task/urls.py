from django.urls import path
from .views import TaskListView, TaskView, TaskImagesView, AddAswerView, AnswerListView, AnswerView

urlpatterns = [
    path('task/', TaskListView.as_view()),
    path('task/image/<int:pk>/', TaskImagesView.as_view()),
    path('task/answer/add/', AddAswerView.as_view()),
    path('task/<int:pk>/', TaskView.as_view()),
    path('task/aswer/', AnswerListView.as_view()),
    path('task/answer/<int:pk>', AnswerView.as_view())
]