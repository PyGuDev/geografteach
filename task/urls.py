from django.urls import path
from .views import TaskListView, TaskView, TaskImagesView, AddAnswerView, AnswerListView, AnswerView, ListTestView, \
    TestView, CreateTestResultView, CreateTestSessionView

urlpatterns = [
    path('task/', TaskListView.as_view()),
    path('task/<int:task_pk>/', TaskView.as_view()),
    path('task/<int:task_pk>/answer/', AnswerView.as_view()),
    path('task/image/<int:pk>/', TaskImagesView.as_view()),
    path('task/answer/add/', AddAnswerView.as_view()),
    path('test/', ListTestView.as_view(), name='list_test'),
    path('test/<slug:test_pk>/session', CreateTestSessionView.as_view(), name='create_test_session'),
    path('test/<slug:test_pk>/session/<int:session_pk>', TestView.as_view(), name='detail_test'),
    path('test/<slug:test_pk>/session/<int:session_pk>/result', CreateTestResultView.as_view(), name='result_test'),

    # path('task/<int:task_pk>/answer/<int:answer_pk>', AnswerView.as_view())
]