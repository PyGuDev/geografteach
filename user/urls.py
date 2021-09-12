from django.urls import path
from .views import SignUpUserAPIView, ConfirmUserAPIView, SingInAPIView, GetUserAPIView

urlpatterns = [
    path('register/', SignUpUserAPIView.as_view(), name='register'),
    path('confirm/', ConfirmUserAPIView.as_view(), name='confirm'),
    path('singin/', SingInAPIView.as_view(), name='sing_in'),
    path('profile/', GetUserAPIView.as_view(), name='profile')
]