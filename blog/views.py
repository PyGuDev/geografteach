import django_filters
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from django_project.response import AccessResponse
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .actions import LikeArticle
from .models import Article, Category, File, ImagesForArticle
from .serializer import CategorySerializer, ArticleSerializer, FileListSerializer, \
    ImagesForArticleSerializer
from .service import PaginationApp, get_client_ip
from .filters import ArticleFilter


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


class ImagesForArticleView(generics.ListAPIView):
    """Вывод списка изображений для поста"""
    serializer_class = ImagesForArticleSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = ImagesForArticle.objects.filter(article=self.request.GET['id'])
        return queryset


class SingleArticleView(generics.RetrieveAPIView):
    """Вывод детальной информации и посте"""
    serializer_class = ArticleSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Article.objects.get_article_with_likes(self.request)

    def get_object(self):
        obj = super().get_object()
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
