# Generated by Django 4.0 on 2022-01-02 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20210912_1057'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='chat',
            table='chat',
        ),
        migrations.AlterModelTable(
            name='message',
            table='message',
        ),
    ]