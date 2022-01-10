# Generated by Django 4.0 on 2022-01-07 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_alter_answer_table_alter_imagetask_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание ответа'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='task.task', verbose_name='Задание'),
        ),
    ]
