from django.db import models


class Category(models.Model):
    """Категория"""
    name = models.CharField('Название', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    """Пост"""
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField('Заголовок', max_length=255, blank=False)
    text = models.TextField('Текст', blank=False)
    img = models.ImageField('Изображение', blank=True)
    url_youtube = models.URLField('Ссылка на ютуб видео', blank=True)
    is_available = models.BooleanField('Активно', default=True)
    pub_date = models.DateField('Дата публикации', auto_now_add=True, blank=True)
    visit = models.IntegerField('Просмотры', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'


class ImagesForArticle(models.Model):
    """Модель изображения для постов"""
    img = models.ImageField('Изображение', upload_to='uploads/images/article/', blank=True)
    article = models.ForeignKey(Article, verbose_name='Пост', on_delete=models.CASCADE)

    def __str__(self):
        return self.img.name

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Like(models.Model):
    """Лайки"""
    ip = models.CharField('IP адресс', max_length=15)
    like = models.BooleanField('Нравится')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Пост', related_name="likes")

    def __str__(self):
        return f"{self.like} - {self.article}"

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"


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
