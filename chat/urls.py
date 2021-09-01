from django.urls import path
from .views import CreateMessageView, ListMessageToUser, ListMessageToAdmin

urlpatterns = [
    path('create/', CreateMessageView.as_view()),
    path('toUser/', ListMessageToUser.as_view()),
    path('toAdmin/', ListMessageToAdmin.as_view())
]
