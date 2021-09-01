from django.urls import path
from .views import SingupUser, ConfirmUser, SingIn, Logout, GetUser

urlpatterns = [
    path('register/', SingupUser.as_view()),
    path('confirm/', ConfirmUser.as_view()),
    path('singin/', SingIn.as_view()),
    path('logout/', Logout.as_view()),
    path('<int:pk>/', GetUser.as_view())
]