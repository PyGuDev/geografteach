from django.db.models import Q
from django_filters import rest_framework as filters
from .models import Article, File


class ArticleFilter(filters.FilterSet):

    category = filters.CharFilter(field_name='category__id', lookup_expr='icontains')
    q = filters.CharFilter(method='search')

    def search(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(title__icontains=value) | Q(text__icontains=value))
        return queryset

    class Meta:
        model = Article
        fields = ['category', 'pub_date']


class FileFilter(filters.FilterSet):
    q = filters.CharFilter(method='search')

    def search(self, queryset, name, value):
        if value:
            queryset = queryset.filter(
                Q(title__icontains=value) | Q(tags__title__icontains=value) | Q(description__icontains=value)
            )
        return queryset

    class Meta:
        model = File
        fields = ['title']
