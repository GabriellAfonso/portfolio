from django.urls import path, include
from webchat.views import views
from webchat.views import rest


app_name = 'webchat'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('singup/', views.singup, name='singup'),
    path('logout/', views.logout_view, name='logout'),
    path('get-token/', views.get_token, name='get_token'),
    path('', views.webchat, name='chat'),

    path('api/profile/<int:pk>/', rest.user_profile, name='user_profile'),
]
