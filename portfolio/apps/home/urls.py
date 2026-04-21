from django.urls import URLPattern, URLResolver, path

from apps.home import views

app_name = "home"

urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.index, name="index"),
    path("curriculo/", views.curriculo, name="curriculo"),
]
