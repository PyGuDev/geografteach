# Generated by Django 3.2.7 on 2021-09-05 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20210905_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='is_like',
            field=models.BooleanField(null=True, verbose_name='Нравится'),
        ),
    ]
