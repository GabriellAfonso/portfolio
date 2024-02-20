from django.urls import path, include
from webchat import views



app_name = 'webchat'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('singup/', views.singup, name='singup'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.webchat, name='chat'),
]

