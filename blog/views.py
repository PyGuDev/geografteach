from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.encoding import escape_uri_path
from django.db import models
from .serializer import CategorySerializer, ArticleSerilizer, CreateLikeSerializer, FileListSerializer, ImagesForArticleSerializer
from .models import Article, Category, File, Like, ImagesForArticle
from .service import get_client_ip, PaginationApp


class CategoryView(generics.ListAPIView):
    """Вывод категорий"""
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = ()


class ArticleListView(generics.ListAPIView):
    """Вывод списка постов"""
    serializer_class = ArticleSerilizer
    pagination_class = PaginationApp
    permission_classes = ()

    def get_queryset(self):
        queryset = Article.objects.filter(avilable=True).annotate(
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
    parser_classes = ()
    permission_classes = ()

    def get_queryset(self):
        queryset = ImagesForArticle.objects.filter(article=self.request.GET['id'])
        return queryset


class ArticleFilterView(generics.ListAPIView):
    """Вывод списка постов для фильтрации"""
    serializer_class = ArticleSerilizer
    permission_classes = ()

    def get_queryset(self):
        queryset = Article.objects.filter(avilable=True).annotate(
            like_user=models.Count(
                "likes",
                filter=models.Q(likes__ip=get_client_ip(self.request), likes__like=True)
            )
        ).annotate(
            count_like=models.Count('likes', filter=models.Q(likes__like=True))
        )
        print(self.request)
        return queryset


class SingleArticleView(generics.RetrieveAPIView):
    """Вывод детальной информации и посте"""
    serializer_class = ArticleSerilizer
    permission_classes = ()

    def get_queryset(self):
        queryset = Article.objects.filter(avilable=True).annotate(
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
    permission_classes = ()

    def perform_create(self, serializer):
        print(self.request.POST)
        serializer.save(ip=get_client_ip(self.request))


class FileListView(generics.ListAPIView):
    """Вывод списка файлов"""
    serializer_class = FileListSerializer
    queryset = File.objects.all().order_by('-pk')
    permission_classes = ()


class FileDownLoadView(APIView):
    """Загрузка файлов"""
    permission_classes = ()

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
        response['Content-Disposition'] = "attachment; filename=" + escape_uri_path(file_name+'.'+file_type)

        return response




