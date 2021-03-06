from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from rest_framework.request import Request

from blog.service import get_client_ip


class Category(models.Model):
    """Категория"""
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        db_table = "category"


class ArticleManager(models.Manager):
    def get_article_with_likes(self, request: Request):
        return self.model.objects.filter(is_available=True).annotate(
            like_user=models.Count(
                "likes",
                filter=models.Q(likes__ip=get_client_ip(request), likes__is_like=True)
            )
        ).annotate(
            count_like=models.Count('likes', filter=models.Q(likes__is_like=True))
        ).order_by('-pub_date')


class Article(models.Model):
    """Пост"""
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField('Заголовок', max_length=255, blank=False)
    text = RichTextUploadingField(config_name='default', verbose_name='Текст')
    img = models.ImageField('Изображение', upload_to='uploads/article/', blank=True)
    url_youtube = models.URLField('Ссылка на ютуб видео', blank=True)
    is_available = models.BooleanField('Активно', default=True)
    pub_date = models.DateField('Дата публикации', auto_now_add=True, blank=True)
    visit = models.IntegerField('Просмотры', default=0)

    objects = ArticleManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'
        db_table = "article"


class ImagesForArticle(models.Model):
    """Модель изображения для постов"""
    img = models.ImageField('Изображение', upload_to='uploads/images/article/', blank=True)
    article = models.ForeignKey(Article, verbose_name='Пост', related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.img.name

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        db_table = "image"


class Like(models.Model):
    """Лайки"""
    ip = models.CharField('IP адресс', max_length=15)
    is_like = models.BooleanField('Нравится', null=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Пост', related_name="likes")

    def __str__(self):
        return f"{self.is_like} - {self.article}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"
        db_table = "like"


class File(models.Model):
    """Файл"""
    title = models.CharField('Название', max_length=120)
    description = models.TextField('Описание файла')
    file = models.FileField('Файл', upload_to='uploads/files/')
    size = models.CharField('Размер файла', max_length=255, blank=True)
    type_file = models.CharField('Формат файла', max_length=20, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['-pk']
        db_table = "file"

    # Переопределил метод save для сохранения размера файла
    def save(self, *args, **kwargs):
        if self.file.file.size > 1024:
            self.size = str(round(self.file.file.size / 1024, 1)) + ' кб'
        elif self.file.file.size / 1024 > 1024:
            self.size = str(round((self.file.file.size / 1024) / 1024, 1)) + 'мб'
        elif self.file.file.size < 1024:
            self.size = str(self.file.file.size) + ' байт'
        self.type_file = str(self.file).split('/')[-1].split('.')[-1]
        super().save(*args, **kwargs)


class TagFile(models.Model):
    title = models.CharField('Название', max_length=300)
    file = models.ForeignKey('File', on_delete=models.CASCADE, related_name='tags')

    def __int__(self):
        return self.title

    class Meta:
        verbose_name = 'Тэг для файла'
        verbose_name_plural = 'Тэги для файлов'
        db_table = "tag_file"
