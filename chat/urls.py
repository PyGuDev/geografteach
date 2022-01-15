from django.urls import path
from .views import CreateMessageAPIView, ListMessageAPIView


urlpatterns = [
    path('message/', ListMessageAPIView.as_view(), name='list_message'),
    path('message/create/', CreateMessageAPIView.as_view(), name='create_message')
]
