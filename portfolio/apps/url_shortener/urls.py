from django.urls import path, include
from . import views


app_name = 'url_shortener'

urlpatterns = [

    path('', views.ShortenUrl.as_view(), name='shorten-url'),
    path('login/', views.Login.as_view(), name='login'),
    path('singup/', views.SingUp.as_view(), name='singup'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
