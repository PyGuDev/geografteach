from django.contrib import admin
from .models import MessageUser, MessageAdmin


class MassageToUserInline(admin.TabularInline):
    model = MessageAdmin
    extra = 0


@admin.register(MessageAdmin)
class MessageToUser(admin.ModelAdmin):
    list_display = ('id', 'text', 'to_message')
    list_filter = ['to_message']
    list_display_links = ('id', 'text')


@admin.register(MessageUser)
class MessageUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author')
    list_filter = ['author']
    list_display_links = ('id', 'text')
    inlines = [MassageToUserInline]


