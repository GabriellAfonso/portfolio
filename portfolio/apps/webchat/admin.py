from django.contrib import admin
from .models import Profile, ChatRoom, Message

admin.site.register(Profile)
admin.site.register(ChatRoom)
admin.site.register(Message)
