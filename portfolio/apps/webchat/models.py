import os
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.templatetags.static import static
from PIL import Image


DEFAULT_PROFILE_PICTURE = '../static/webchat/images/icons/empty_picture.jpg'


def get_profile_picture_path(instance, filename):
    ext = filename.split('.')[-1]
    # Nome fixo baseado no usuário
    filename = f"profile_picture_{instance.user.id}.{ext}"
    return os.path.join('webchat/profile_picture/', filename)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=50)
    profile_picture = models.ImageField(
        upload_to=get_profile_picture_path, blank=True, default=DEFAULT_PROFILE_PICTURE)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def resize_profile_picture(self):
        """Redimensiona a foto de perfil para 200x200 se não for a padrão."""
        if not self.profile_picture or 'empty_picture.jpg' in self.profile_picture.name:
            return
        try:
            img = Image.open(self.profile_picture.path)
            img = img.resize((200, 200))
            img.save(self.profile_picture.path)
        except FileNotFoundError:
            pass

    # TODO fazer o profile picture voltar ao default se a imagem do usuario for deletada do sistema de arquivos
    # TODO deletar imagem antiga ao trocar a imagem de perfil


class ChatRoom(models.Model):
    members = models.ManyToManyField(Profile, related_name='chat_rooms')

    def __str__(self):
        return f'room:{self.id}'


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Verifica se o remetente está entre os membros da sala de chat
        if self.sender not in self.room.members.all():
            raise PermissionDenied(
                "Você não tem permissão para enviar mensagens para esta sala de chat.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f'id:{self.id} {self.room}'
