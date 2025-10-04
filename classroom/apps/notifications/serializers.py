from rest_framework import serializers
from .models import Notification
from apps.authorization.serializers import UserProfileSerializer


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class NotificationListSerializer(serializers.ModelSerializer):
    sender = UserProfileSerializer(read_only=True)  # Из authorization

    class Meta:
        model = Notification
        fields = ('id', 'title', 'message', 'sender', 'created_at', 'is_read')
        read_only_fields = ('sender', 'created_at')