from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserInfoView

auth_urlpatterns = [
    path('sign_up/', UserRegistrationView.as_view(), name='sign_up'),
    path('sign_in/', TokenObtainPairView.as_view(), name='sign_in'),  # получает пару токенов
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # обновляет токен
]

urlpatterns = [
    path('auth/', include(auth_urlpatterns), name='auth'),
    path('me/', UserInfoView.as_view(), name='me'),
]
