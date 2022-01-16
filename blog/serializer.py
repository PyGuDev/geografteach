from django.utils.html import strip_tags
from rest_framework import serializers

from django_project.settings import SERVER_URL
from .models import Article, Category, Like, File, ImagesForArticle, TagFile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SingleArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class TagsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagFile
        fields = ['title']


class ArticleSerializer(serializers.ModelSerializer):
    """Сериализация постов"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    like_user = serializers.BooleanField()
    count_like = serializers.IntegerField()
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    images = serializers.SerializerMethodField('get_images')
    pub_date = serializers.DateField(format="%d.%m.%Y")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['text'] = instance.text.replace('/media/uploads', f'{SERVER_URL}/media/uploads')
        return data

    def get_images(self, obj: Article):
        images = obj.images.all()
        return ImagesForArticleSerializer(instance=images).data

    class Meta:
        model = Article
        fields = (
            'id',
            'category',
            'title',
            'text',
            'img',
            'url_youtube',
            'is_available',
            'pub_date',
            'visit',
            'like_user',
            'count_like',
            'images'
        )


class ImagesForArticleSerializer(serializers.ModelSerializer):
    """Сериалайзер изображений для постов"""
    class Meta:
        model = ImagesForArticle
        fields = ['img']


class FileListSerializer(serializers.ModelSerializer):
    """Сериалайзер файлов"""
    tags = serializers.SerializerMethodField('get_tags')

    def get_tags(self, obj):
        files = obj.tags.all()
        return TagsFileSerializer(instance=files, many=True, read_only=True).data

    class Meta:
        model = File
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер категорий"""

    class Meta:
        model = Category
        fields = ('id', 'name')
