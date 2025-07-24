from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Notification, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone')


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('date_sent', 'status')
