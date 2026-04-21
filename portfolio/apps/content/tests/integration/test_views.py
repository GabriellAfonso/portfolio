import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import resolve, reverse

from apps.content import views
from apps.content.models import AboutMe, Project, Resume


@pytest.mark.integration
class ResumeUrlTest(TestCase):
    def test_resume_url_path(self) -> None:
        assert reverse("content:resume") == "/curriculo/"

    def test_resume_url_resolves(self) -> None:
        assert resolve("/curriculo/").func == views.resume_download


@pytest.mark.integration
class ResumeViewTest(TestCase):
    def test_returns_404_when_no_file(self) -> None:
        Resume.load()
        response = Client().get(reverse("content:resume"))
        assert response.status_code == 404

    def test_returns_pdf_when_file_uploaded(self) -> None:
        resume = Resume.load()
        resume.file_pt = SimpleUploadedFile(
            "cv.pdf", b"%PDF-1.4 content", content_type="application/pdf"
        )
        resume.save()
        response = Client().get(reverse("content:resume"))
        assert response.status_code == 200
        assert response["Content-Type"] == "application/pdf"


@pytest.mark.integration
class IndexLanguageTest(TestCase):
    def setUp(self) -> None:
        AboutMe.objects.create(content_pt="sobre pt text", content_en="about en text")
        Project.objects.create(
            title_pt="Projeto BR",
            title_en="English Project",
            short_description_pt="desc pt",
            short_description_en="desc en",
            project_url="https://example.com",
        )

    def test_pt_root_renders_portuguese_content(self) -> None:
        response = Client().get("/")
        assert response.status_code == 200
        assert b"Projeto BR" in response.content
        assert b"sobre pt text" in response.content
        assert b"English Project" not in response.content

    def test_en_prefix_renders_english_content(self) -> None:
        response = Client().get("/en/")
        assert response.status_code == 200
        assert b"English Project" in response.content
        assert b"about en text" in response.content
        assert b"Projeto BR" not in response.content
