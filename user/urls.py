from django.urls import path
from .views import SignUpUser, ConfirmUser, SingIn, Logout, GetUser

urlpatterns = [
    path('register/', SignUpUser.as_view()),
    path('confirm/', ConfirmUser.as_view()),
    path('singin/', SingIn.as_view()),
    path('logout/', Logout.as_view()),
    path('<int:pk>/', GetUser.as_view())
]