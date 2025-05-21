from django.urls import path, include
from apps.home import views


app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('guest/<str:app_name>/', views.guest_login, name='guest_login'),
    path('curriculo/', views.curriculo, name='curriculo'),

]
