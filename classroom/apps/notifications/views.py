from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import NotificationSerializer, NotificationListSerializer
from .models import Notification


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read', 'created_at', 'recipient']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return NotificationListSerializer
        return NotificationSerializer

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)

    @action(detail=False, methods=['get'])
    def unread(self, request):
        queryset = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        if notification.recipient != request.user:
            raise permissions.PermissionDenied("You can only mark your own notifications as read")
        notification.is_read = True
        notification.save()
        return Response({'status': 'read'})