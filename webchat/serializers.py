import os
from rest_framework import serializers
from .models import Profile, ChatRoom, Message


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25, required=False)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'profile_picture']


class ChatRoomSerializer(serializers.ModelSerializer):

    members = ProfileSerializer(many=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'members']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
