from django.db import models
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Category, File, ImagesForArticle
from .serializer import CategorySerializer, ArticleSerializer, CreateLikeSerializer, FileListSerializer, \
    ImagesForArticleSerializer
from .service import get_client_ip, PaginationApp


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

    def get_queryset(self):
        queryset = Article.objects.filter(is_available=True).annotate(
            like_user=models.Count(
                "likes",
                filter=models.Q(likes__ip=get_client_ip(self.request), likes__like=True)
            )
        ).annotate(
            count_like=models.Count('likes', filter=models.Q(likes__like=True))
        ).order_by('pk')
        return queryset


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
        queryset = Article.objects.filter(is_available=True).annotate(
            like_user=models.Count(
                "likes",
                filter=models.Q(likes__ip=get_client_ip(self.request), likes__like=True)
            )
        ).annotate(
            count_like=models.Count('likes', filter=models.Q(likes__like=True))
        )
        pk = self.request.path.rsplit('/')[-2]
        obj = queryset.get(pk=pk)
        obj.visit += 1
        obj.save()
        return queryset


class AddLikeArticleView(generics.CreateAPIView):
    """Добовление лайков"""
    serializer_class = CreateLikeSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        print(self.request.POST)
        serializer.save(ip=get_client_ip(self.request))


class FileListView(generics.ListAPIView):
    """Вывод списка файлов"""
    serializer_class = FileListSerializer
    queryset = File.objects.all().order_by('-pk')
    permission_classes = (permissions.AllowAny,)


class FileDownLoadView(APIView):
    """Загрузка файлов"""
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        file_id = request.GET.__getitem__('id')
        try:
            obj_file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            return Response(status=400, data={"error": "Такого файла не существует"})

        file = open(obj_file.file.path, 'rb').read()
        file_name = obj_file.title
        file_type = obj_file.type_file
        response = HttpResponse(file, content_type='application/{}'.format(file_type))
        response['Content-Disposition'] = "attachment; filename=" + escape_uri_path(file_name + '.' + file_type)

        return response
