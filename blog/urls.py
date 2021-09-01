from django.urls import path
from .views import CategoryView, ArticleListView, ImagesForArticleView, ArticleFilterView, SingleArticleView, AddLikeArticleView, FileListView, FileDownLoadView


urlpatterns = [
    path('blog/filter/', ArticleFilterView.as_view()),
    path('blog/', ArticleListView.as_view()),
    path('blog/article/<int:pk>/', SingleArticleView.as_view()),
    path('blog/addLike', AddLikeArticleView.as_view()),
    path('blog/category/', CategoryView.as_view()),
    path('blog/images/', ImagesForArticleView.as_view()),
    path('blog/files/', FileListView.as_view()),
    path('download/file/', FileDownLoadView.as_view()),
]
