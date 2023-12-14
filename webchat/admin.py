from django.contrib import admin
from .models import Profile, ChatRoom, Message

# Registre os modelos no painel administrativo
admin.site.register(Profile)
admin.site.register(ChatRoom)
admin.site.register(Message)

