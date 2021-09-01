from django.contrib import admin
from .models import Task, ImageTask, Answer


class ImageTaskInline(admin.TabularInline):
    model = ImageTask
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ['avilable', 'class_student']
    list_display = ('id', 'title', 'date', 'avilable', 'class_student')
    search_fields = ['title']
    list_display_links = ('id', 'title')
    inlines = [ImageTaskInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_filter = ('task', 'author', 'estimation')
    list_display = ('id', 'author', 'file_answer', 'task', 'estimation')
    list_display_links = ('id', 'author')


admin.site.register(ImageTask)
