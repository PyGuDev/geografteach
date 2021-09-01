from rest_framework import serializers
from .models import MessageUser, MessageAdmin


class MessagesToAdminSerializer(serializers.ModelSerializer):
    """Сериализатор сообщений админу"""

    class Meta:
        model = MessageUser
        fields = "__all__"


class MessagesToUserSerializer(serializers.ModelSerializer):
    """Сериализатор сообщений пользователям"""

    class Meta:
        model = MessageAdmin
        fields = "__all__"