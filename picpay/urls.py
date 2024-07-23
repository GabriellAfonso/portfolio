from django.contrib import admin
from django.urls import path, include
from .views import Login, Register, YourProfile, Logout
from .rest_views import TransactionRest


app_name = 'picpay'

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('cadastro/', Register.as_view(), name='register'),
    path('Seu-perfil/', YourProfile.as_view(), name='profile'),
    path('logout/', Logout.as_view(), name='logout'),
    path('api/transaction/', TransactionRest.as_view(), name='api_transaction'),
]
