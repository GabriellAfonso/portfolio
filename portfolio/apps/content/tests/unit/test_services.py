import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.content.models import AboutMe, Project, Resume
from apps.content.repositories.about_repository import AboutRepository
from apps.content.repositories.project_repository import ProjectRepository
from apps.content.repositories.resume_repository import ResumeRepository
from apps.content.services.about_service import AboutService
from apps.content.services.project_service import ProjectService
from apps.content.services.resume_service import ResumeService


@pytest.mark.unit
@pytest.mark.django_db
class TestProjectService:
    def _create(self, **overrides: object) -> Project:
        defaults: dict[str, object] = {
            "title_pt": "Projeto",
            "title_en": "Project",
            "short_description_pt": "desc pt",
            "short_description_en": "desc en",
            "project_url": "https://example.com",
        }
        defaults.update(overrides)
        return Project.objects.create(**defaults)

    def test_list_active_filters_inactive(self) -> None:
        self._create(title_pt="Ativo", is_active=True)
        self._create(title_pt="Inativo", is_active=False)
        service = ProjectService(ProjectRepository())
        result = service.list_active("pt-br")
        titles = [p["title"] for p in result]
        assert "Ativo" in titles
        assert "Inativo" not in titles

    def test_list_active_returns_portuguese_for_pt(self) -> None:
        self._create()
        service = ProjectService(ProjectRepository())
        result = service.list_active("pt-br")
        assert result[0]["title"] == "Projeto"
        assert result[0]["short_description"] == "desc pt"

    def test_list_active_returns_english_for_en(self) -> None:
        self._create()
        service = ProjectService(ProjectRepository())
        result = service.list_active("en")
        assert result[0]["title"] == "Project"
        assert result[0]["short_description"] == "desc en"


@pytest.mark.unit
@pytest.mark.django_db
class TestAboutService:
    def test_returns_pt_content(self) -> None:
        AboutMe.objects.create(content_pt="pt text", content_en="en text")
        service = AboutService(AboutRepository())
        assert service.get("pt-br") == "pt text"

    def test_returns_en_content(self) -> None:
        AboutMe.objects.create(content_pt="pt text", content_en="en text")
        service = AboutService(AboutRepository())
        assert service.get("en") == "en text"


@pytest.mark.unit
@pytest.mark.django_db
class TestResumeService:
    def test_returns_none_when_no_file(self) -> None:
        Resume.load()
        service = ResumeService(ResumeRepository())
        assert service.get_file("pt-br") is None

    def test_returns_pt_file(self) -> None:
        resume = Resume.load()
        resume.file_pt = SimpleUploadedFile("cv_pt.pdf", b"%PDF pt", content_type="application/pdf")
        resume.save()
        service = ResumeService(ResumeRepository())
        assert service.get_file("pt-br") is not None

    def test_returns_en_file(self) -> None:
        resume = Resume.load()
        resume.file_en = SimpleUploadedFile("cv_en.pdf", b"%PDF en", content_type="application/pdf")
        resume.save()
        service = ResumeService(ResumeRepository())
        assert service.get_file("en") is not None
