from django.contrib import admin
from django.urls import path, include
from .views import Login, Register, Profile


app_name = 'picpay'

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('cadastro', Register.as_view(), name='register'),
    path('Seu-perfil', Profile.as_view(), name='profile'),
]
