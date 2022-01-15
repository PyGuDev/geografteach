from django.contrib import admin
from .models import Category, Article, Like, File, ImagesForArticle, TagFile


class ImagesForArticleInline(admin.TabularInline):
    model = ImagesForArticle
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_filter = ('category', 'is_available')
    list_display = ('id', 'title', 'category', 'pub_date', 'is_available')
    list_display_links = ('id', 'title')
    inlines = [ImagesForArticleInline]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_filter = ('is_like', 'ip')
    list_display = ('is_like', 'ip', 'article')


class TagFileInline(admin.TabularInline):
    model = TagFile
    extra = 0


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'size', 'type_file')
    list_filter = ['type_file']
    inlines = [TagFileInline]


@admin.register(TagFile)
class TagFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'file']
    list_display_links = ['id', 'title']


admin.site.register(Category)
admin.site.register(ImagesForArticle)
