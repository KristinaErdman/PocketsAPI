from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistration, MeView


urlpatterns = [
    path('sign_up/', UserRegistration.as_view(), name='sign_up'),
    path('sign_in/', TokenObtainPairView.as_view(), name='sign_in'),  # получает пару токенов
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # обновляет токен
    path('me/', MeView.as_view(), name='me'),
]
