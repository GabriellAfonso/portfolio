from django.urls import path, include
from . import views


app_name = 'url_shortener'

urlpatterns = [

    path('', views.ShortenUrl.as_view(), name='shorten-url'),
    path('<str:short_url>/', views.redirect_view, name='redirect_view'),
]
