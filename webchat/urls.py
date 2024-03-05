from django.urls import path, include
from webchat.views import views
from webchat.views import rest


app_name = 'webchat'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('singup/', views.singup, name='singup'),
    path('logout/', views.logout_view, name='logout'),
    path('getToken/', views.get_token, name='get_token'),
    path('', views.webchat, name='chat'),

    path('api/profile/<int:pk>/', rest.user_profile, name='user_profile'),
    path('api/newChatRoom/', rest.create_chatroom, name='new_chat_room'),
    path('api/chatrooms/<int:chatroom_id>/send_message/',
         rest.send_message, name='send_message'),
    path('api/chatrooms/<int:chatroom_id>/view_messages/',
         rest.view_messages, name='view_messages'),
]
