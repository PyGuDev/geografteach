# Generated by Django 4.0 on 2022-01-02 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_merge_0002_auto_20210912_1051_0003_auto_20210911_1543'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='answer',
            table='answer',
        ),
        migrations.AlterModelTable(
            name='imagetask',
            table='image_for_task',
        ),
        migrations.AlterModelTable(
            name='task',
            table='task',
        ),
    ]
