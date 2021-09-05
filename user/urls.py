from django.urls import path
from .views import SignUpUserAPIView, ConfirmUserAPIView, SingInAPIView, GetUserAPIView

urlpatterns = [
    path('register/', SignUpUserAPIView.as_view()),
    path('confirm/', ConfirmUserAPIView.as_view()),
    path('singin/', SingInAPIView.as_view()),
    path('<int:pk>/', GetUserAPIView.as_view())
]