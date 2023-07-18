from django.urls import path, include
from portifolio import views


app_name = 'portifolio'

urlpatterns = [
    path('', views.index, name='index'),
]
