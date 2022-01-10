# Generated by Django 4.0 on 2022-01-07 18:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('task', '0006_alter_answer_description_alter_answer_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='PossibleQuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(verbose_name='Ответ на вопрос')),
                ('is_current', models.BooleanField(blank=True, default=False, verbose_name='Правильный?')),
            ],
            options={
                'verbose_name': 'Вопрос к тесту',
                'verbose_name_plural': 'Вопросы к тесту',
                'db_table': 'possible_answer',
            },
        ),
        migrations.CreateModel(
            name='TestQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Текст вопроса')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение для вопроса')),
            ],
            options={
                'verbose_name': 'Вопросы к тесту',
                'verbose_name_plural': 'Вопросы к тесту',
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='TestSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='Время начала')),
                ('end_time', models.DateTimeField(verbose_name='Время завершения')),
                ('result', models.DecimalField(blank=True, decimal_places=1, max_digits=4, verbose_name='Результат в процентах')),
            ],
            options={
                'verbose_name': 'Вопрос к тесту',
                'verbose_name_plural': 'Вопросы к тесту',
                'db_table': 'test_session',
            },
        ),
        migrations.CreateModel(
            name='TestTask',
            fields=[
                ('uid', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=300, verbose_name='Название')),
                ('duration_session', models.DurationField(verbose_name='Время на прохождение')),
                ('expiry_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания действия')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
                'db_table': 'test',
            },
        ),
        migrations.CreateModel(
            name='UserAnswerForQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answer', to='task.possiblequestionanswer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answer', to='task.testquestion')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answer', to='task.testsession')),
            ],
            options={
                'verbose_name': 'Ответ пользователя',
                'verbose_name_plural': 'Ответы пользователя',
                'db_table': 'user_answer',
            },
        ),
        migrations.AddField(
            model_name='testsession',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_sessions', to='task.testtask'),
        ),
        migrations.AddField(
            model_name='testsession',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AddField(
            model_name='testquestion',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='task.testtask'),
        ),
        migrations.AddField(
            model_name='possiblequestionanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='task.testquestion'),
        ),
    ]
