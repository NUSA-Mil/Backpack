from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import LoginView, logout_view, CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    # Аутентификация
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_view, name="logout"),

    # Стандартные токены
    path('token/', obtain_auth_token, name='api_token_auth'),

    # JWT токены
    path('jwt/token/', TokenObtainPairView.as_view(), name='jwt_token_obtain'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='jwt_token_refresh'),

    # API для пользователей
    path('', include(router.urls)),
]