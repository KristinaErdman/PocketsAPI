from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', )

    def create(self, validated_data):
        new_user = super(CustomUserSerializer, self).create(validated_data)
        new_user.set_password(validated_data['password'])
        new_user.save()
        return new_user
