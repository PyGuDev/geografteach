# Generated by Django 3.2.7 on 2021-09-14 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_like_is_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagesforarticle',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.article', verbose_name='Пост'),
        ),
    ]
