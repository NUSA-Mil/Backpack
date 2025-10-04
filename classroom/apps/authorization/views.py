from django.contrib.auth import login, logout
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import generics, viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import LoginUserSerializer, UserProfileSerializer, CustomUserSerializer, UserAvatarSerializer
from .models import CustomUser

class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)

        return Response({
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({
        "message": "Logout successful"
    }, status=status.HTTP_200_OK)


#ViewSet для пользователей
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role_id', 'is_active', 'email']

    #Эндпоинт для обновления аватара
    @action(detail=False, methods=["put"])
    def update_avatar(self, request):
        user = request.user
        serializer = UserAvatarSerializer(user, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

