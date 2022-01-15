import django_filters
from django_project.response import AccessResponse
from rest_framework import generics
from rest_framework import permissions

from .actions import LikeArticle
from .models import Article, Category, File
from .serializer import CategorySerializer, ArticleSerializer, FileListSerializer
from .service import PaginationApp
from .filters import ArticleFilter, FileFilter


class CategoryView(generics.ListAPIView):
    """Вывод категорий"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny,)


class ArticleListView(generics.ListAPIView):
    """Вывод списка постов"""
    serializer_class = ArticleSerializer
    pagination_class = PaginationApp
    permission_classes = (permissions.AllowAny,)
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = ArticleFilter

    def get_queryset(self):
        return Article.objects.get_article_with_likes(self.request)


class SingleArticleView(generics.RetrieveAPIView):
    """Вывод детальной информации и посте"""
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Article.objects.get_article_with_likes(self.request)

    def get_object(self):
        obj = super().get_object()
        print(obj.text)
        obj.visit += 1
        obj.save()
        return obj


class AddLikeArticleView(generics.CreateAPIView):
    """Добовление лайков"""
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        data = LikeArticle(request, self.kwargs.get('pk')).add_like()
        return AccessResponse(data)


class FileListView(generics.ListAPIView):
    """Вывод списка файлов"""
    serializer_class = FileListSerializer
    queryset = File.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = PaginationApp
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = FileFilter
