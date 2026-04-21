from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import get_language

from apps.content.repositories.about_repository import AboutRepository
from apps.content.repositories.project_repository import ProjectRepository
from apps.content.services.about_service import AboutService
from apps.content.services.project_service import ProjectService


def index(request: HttpRequest) -> HttpResponse:
    language = get_language() or "pt-br"
    context = {
        "projects": ProjectService(ProjectRepository()).list_active(language),
        "about_content": AboutService(AboutRepository()).get(language),
    }
    return render(request, "home/index.html", context)
