from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from core.models import Notification, User
from .serializers import NotificationSerializer, UserSerializer
from .service import SendNotification


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        notification = Notification.objects.get(id=serializer.data['id'])
        SendNotification.send_notification(notification)

        response_data = self.get_serializer(notification).data
        return Response(
            response_data, status=status.HTTP_201_CREATED
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
