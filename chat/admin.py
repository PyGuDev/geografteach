from django.contrib import admin
from .models import Message, Chat


class MassageInline(admin.TabularInline):
    model = Message
    extra = 0


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'student')
    inlines = [MassageInline]
