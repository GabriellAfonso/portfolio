from django.urls import path, include
from .views import Home, Tables, RegisterSundays, FindMusic


app_name = 'igreja'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('tabelas', Tables.as_view(), name='tabela'),
    path('registrar-domingo', RegisterSundays.as_view(), name='register_sundays'),
    path('encontrar-musicas', FindMusic.as_view(), name='find_music'),
]
