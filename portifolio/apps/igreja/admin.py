from django.contrib import admin
from apps.igreja.models import Category, Music, Played

admin.site.register(Category)
admin.site.register(Music)
admin.site.register(Played)
