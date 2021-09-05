from rest_framework import serializers
from .models import Article, Category, Like, File, ImagesForArticle


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SingleArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """Сериализация постов"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    like_user = serializers.BooleanField()
    count_like = serializers.IntegerField()
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

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
        )


class ImagesForArticleSerializer(serializers.ModelSerializer):
    """Сериалайзер изображений для постов"""
    class Meta:
        model = ImagesForArticle
        fields = "__all__"


class FileListSerializer(serializers.ModelSerializer):
    """Сериалайзер файлов"""
    class Meta:
        model = File
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер категорий"""

    class Meta:
        model = Category
        fields = ('id', 'name')

