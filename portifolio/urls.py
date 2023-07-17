from django.urls import path
from portifolio import views


app_name = 'portifolio'

urlpatterns = [
    path('', views.index, name='index'),
]
