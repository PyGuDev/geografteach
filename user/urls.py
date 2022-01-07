from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignUpUserAPIView, ConfirmUserAPIView, SingInAPIView, GetUserAPIView, RefreshTokenAPIView

urlpatterns = [
    path('register/', SignUpUserAPIView.as_view(), name='register'),
    path('confirm/', ConfirmUserAPIView.as_view(), name='confirm'),
    path('singin/', SingInAPIView.as_view(), name='sing_in'),
    path('token/refresh', RefreshTokenAPIView.as_view(), name='refresh_token'),
    path('profile/', GetUserAPIView.as_view(), name='profile')
]