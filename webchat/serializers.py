import os
from rest_framework import serializers
from .models import Profile, ChatRoom, Message


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25, required=False)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'profile_picture']

    # def validate_user_name(self, value):
    #     if Profile.objects.filter(user_name=value).exists():
    #         raise serializers.ValidationError(
    #             "Este nome de usuário já está em uso. Por favor, escolha outro.")
    #     return value


class ChatRoomSerializer(serializers.ModelSerializer):
    # Incorporar o ProfileSerializer para serializar os membros
    members = ProfileSerializer(many=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'members']

    # def validate_user_name(self, value):
    #     if Profile.objects.filter(user_name=value).exists():
    #         raise serializers.ValidationError(
    #             "Este nome de usuário já está em uso. Por favor, escolha outro.")
    #     return value


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
