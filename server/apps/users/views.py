from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCreateSerializer, UserRetrieveSerializer
from .models import CustomUser


class UserRegistrationView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer


class UserInfoView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserRetrieveSerializer

    def get_object(self):
        return self.request.user
