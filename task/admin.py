from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html

from .models import Task, ImageTask, Answer, TestTask, TestQuestion, TestSession, PossibleQuestionAnswer,\
    UserAnswerForQuestion


class ImageTaskInline(admin.TabularInline):
    model = ImageTask
    extra = 0


class AnswerForTaskInline(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ['available', 'class_student']
    list_display = ('id', 'title', 'date', 'available', 'class_student')
    search_fields = ['title']
    list_display_links = ('id', 'title')
    inlines = [ImageTaskInline, AnswerForTaskInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_filter = ('task', 'author', 'estimation')
    list_display = ('id', 'author', 'file_answer', 'task', 'estimation')
    list_display_links = ('id', 'author')


class QuestionAnswerInline(admin.TabularInline):
    model = PossibleQuestionAnswer
    extra = 0


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionAnswerInline]
    readonly_fields = ('got_to_test',)

    @admin.display(description="Перейти к тесту")
    def got_to_test(self, obj):
        return format_html(
            f"<a class='button' href='/api/admin/task/testtask/{obj.test.pk}/change/'>Перейти</a>"
        )


@admin.register(PossibleQuestionAnswer)
class PossibleQuestionAnswerAdmin(admin.ModelAdmin):
    pass


class QuestionForm(forms.ModelForm):
    class Meta:
        model = TestQuestion
        fields = '__all__'


class QuestionInline(admin.TabularInline):
    form = QuestionForm
    model = TestQuestion
    extra = 0
    show_change_link = True
    fields = ['question', 'image', 'button']
    readonly_fields = ('button', )

    def button(self, obj):
        return format_html(
            f"<a class='button' href='/api/admin/task/testquestion/{obj.pk}/change/'>Добавить варианты ответов</a>"
        )

    button.allow_tags = True


@admin.register(TestTask)
class TestTaskAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


@admin.register(UserAnswerForQuestion)
class UserAnswerForQuestionAdmin(admin.ModelAdmin):
    pass


class UserAnswerInline(admin.TabularInline):
    model = UserAnswerForQuestion
    extra = 0
    fields = ['question', 'answer']


@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    inlines = [UserAnswerInline]



admin.site.register(ImageTask)
