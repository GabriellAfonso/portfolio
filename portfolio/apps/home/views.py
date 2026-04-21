import os

from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "home/index.html")


def curriculo(request: HttpRequest) -> FileResponse:
    path = os.path.join(settings.BASE_DIR, "apps", "home", "docs", "curriculo.pdf")
    return FileResponse(open(path, "rb"), content_type="application/pdf")
