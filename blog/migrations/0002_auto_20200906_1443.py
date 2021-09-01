# Generated by Django 3.1 on 2020-09-06 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='uploads/files/', verbose_name='Файл'),
        ),
        migrations.CreateModel(
            name='ImagesForArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(blank=True, upload_to='uploads/images/article/', verbose_name='Изображение')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.article', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Изображения',
            },
        ),
    ]
