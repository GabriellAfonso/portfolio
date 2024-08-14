from django.contrib import admin
from .models import Category, Music, Played

admin.site.register(Category)
admin.site.register(Music)
admin.site.register(Played)
