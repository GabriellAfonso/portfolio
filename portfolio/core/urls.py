from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpRequest, JsonResponse
from django.urls import URLPattern, URLResolver, include, path


def health(_request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


urlpatterns: list[URLPattern | URLResolver] = [
    path("health/", health),
    path("", include("apps.home.urls")),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
