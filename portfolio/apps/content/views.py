from django.http import FileResponse, Http404, HttpRequest
from django.utils.translation import get_language

from apps.content.repositories.resume_repository import ResumeRepository
from apps.content.services.resume_service import ResumeService


def resume_download(request: HttpRequest) -> FileResponse:
    service = ResumeService(ResumeRepository())
    file = service.get_file(get_language() or "pt-br")
    if file is None:
        raise Http404("Resume not available")
    return FileResponse(file.open("rb"), content_type="application/pdf")
