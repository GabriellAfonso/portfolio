import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image

DEFAULT_PROFILE_PICTURE = 'webchat/empty_picture.jpg'


def get_profile_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"profile_picture_{instance.user_name}.{ext}"
    return os.path.join('webchat/profile_picture/', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=25, unique=True)
    status = models.CharField(max_length=225, blank=True)
    profile_picture = models.ImageField(upload_to=get_profile_picture_path, blank=True,
                                        null=True, default=DEFAULT_PROFILE_PICTURE)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        try:
            profile = Profile.objects.get(pk=self.pk)
        except Profile.DoesNotExist:
            profile = None

        super(Profile, self).save(*args, **kwargs)

        if profile and profile.profile_picture and profile.profile_picture != self.profile_picture:
            try:
                os.remove(os.path.join(settings.MEDIA_ROOT,
                          str(profile.profile_picture)))
            except FileNotFoundError:
                pass

        if self.profile_picture:
            img = Image.open(self.profile_picture.path)
            img = img.resize((200, 200))
            img.save(self.profile_picture.path)

    def __str__(self):
        return f'id:{self.id} {self.user}'


class ChatRoom(models.Model):
    members = models.ManyToManyField(Profile, related_name='chat_rooms')

    def __str__(self):
        return f'room:{self.id}'


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'id:{self.id} {self.room}'
