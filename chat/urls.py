from django.urls import path
from .views import CreateChatAPIView, CreateMessageAPIView, ListMessageAPIView


urlpatterns = [
    path('create/', CreateChatAPIView.as_view(), name='create_chat'),
    path('<slug:pk>/message/create/', CreateMessageAPIView.as_view(), name='create_message'),
    path('<slug:pk>/message/all/', ListMessageAPIView.as_view(), name='list_message')
]
