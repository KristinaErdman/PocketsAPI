from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer


class UserRegistration(CreateAPIView):
    def post(self, request, *args, **kwargs):
        user_ser = CustomUserSerializer(data=request.data)
        if user_ser.is_valid():
            new_user = user_ser.save()
            return Response({'Status': 'OK'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'Status': 'Error', 'Desc': user_ser.errors}, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'id': request.user.id, 'username': request.user.username}
        print("USER", request.user)
        return Response(content, status=status.HTTP_200_OK)
