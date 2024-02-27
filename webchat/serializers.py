import os
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(max_length=25, required=False)

    class Meta:
        model = Profile
        fields = ['user_name', 'profile_picture']

    # def validate_user_name(self, value):
    #     if Profile.objects.filter(user_name=value).exists():
    #         raise serializers.ValidationError(
    #             "Este nome de usuário já está em uso. Por favor, escolha outro.")
    #     return value
