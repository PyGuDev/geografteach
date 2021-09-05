from django.urls import path
from .views import CategoryView, ArticleListView, ImagesForArticleView, SingleArticleView, \
    AddLikeArticleView, FileListView


urlpatterns = [
    path('blog/', ArticleListView.as_view()),
    path('blog/article/<int:pk>/', SingleArticleView.as_view()),
    path('blog/article/<int:pk>/add_like/', AddLikeArticleView.as_view()),
    path('blog/category/', CategoryView.as_view()),
    path('blog/images/', ImagesForArticleView.as_view()),
    path('blog/files/', FileListView.as_view()),
]
