# Generated by Django 3.2.7 on 2021-09-05 07:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_rename_avilable_article_is_available'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='file',
            options={'ordering': ['-pk'], 'verbose_name': 'Файл', 'verbose_name_plural': 'Файлы'},
        ),
        migrations.RenameField(
            model_name='like',
            old_name='like',
            new_name='is_like',
        ),
    ]
