from django.contrib import admin
from django.urls import path, include
from .views import Login, Register, YourProfile, Logout, start_transaction
from apps.picpay.rest_views import TransactionAPIView


app_name = 'picpay'

urlpatterns = [
    path('', Login.as_view(), name='login'),
    path('cadastro/', Register.as_view(), name='register'),
    path('Seu-perfil/', YourProfile.as_view(), name='profile'),
    path('logout/', Logout.as_view(), name='logout'),
    path('api/transaction/', TransactionAPIView.as_view(), name='api_transaction'),
    path('api/start_transaction/', start_transaction,
         name='start_transaction'),
]
