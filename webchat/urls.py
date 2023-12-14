from django.urls import path, include
from webchat import views


app_name = 'webchat'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('', views.webchat, name='chat'),
]
