import os
from django.db import models
from django.contrib.auth.models import User

def get_profile_picture_path(instance, filename):
    # O nome do arquivo será o user_name seguido pela extensão do arquivo
    ext = filename.split('.')[-1]
    filename = f"profile_picture_{instance.user_name}.{ext}"
    return os.path.join("webchat/profile_picture/", filename)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=25, unique=True)
    status = models.CharField(max_length=225, blank=True)
    profile_picture = models.ImageField(upload_to=get_profile_picture_path, blank=True, null=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f'id:{self.id} {self.user}'


class ChatRoom(models.Model):
    members = models.ManyToManyField(Profile, related_name='chat_rooms')

    def __str__(self):
        return f'id:{self.id} {self.members}'


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return f'id:{self.id} {self.room}'



