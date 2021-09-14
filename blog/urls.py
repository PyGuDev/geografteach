from django.urls import path
from .views import CategoryView, ArticleListView, SingleArticleView, \
    AddLikeArticleView, FileListView


urlpatterns = [
    path('blog/', ArticleListView.as_view(), name='list_article'),
    path('blog/article/<int:pk>/', SingleArticleView.as_view(), name='single_article'),
    path('blog/article/<int:pk>/add_like/', AddLikeArticleView.as_view(), name='add_like'),
    path('blog/category/', CategoryView.as_view(), name='list_category'),
    path('blog/files/', FileListView.as_view(), name='list_files'),
]
