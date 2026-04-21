from django.urls import URLPattern, URLResolver, path

from apps.content import views


app_name = "content"

urlpatterns: list[URLPattern | URLResolver] = [
    path("curriculo/", views.resume_download, name="resume"),
]
