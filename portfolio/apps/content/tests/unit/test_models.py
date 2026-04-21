import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.content.models import AboutMe, Project, Resume


@pytest.mark.unit
@pytest.mark.django_db
class TestProjectModel:
    def test_str_returns_title_pt(self) -> None:
        project = Project.objects.create(
            title_pt="Meu Projeto",
            title_en="My Project",
            short_description_pt="desc pt",
            short_description_en="desc en",
            project_url="https://example.com",
        )
        assert str(project) == "Meu Projeto"

    def test_ordering_by_order_field(self) -> None:
        Project.objects.create(
            title_pt="B",
            title_en="B",
            short_description_pt="",
            short_description_en="",
            project_url="https://example.com",
            order=2,
        )
        Project.objects.create(
            title_pt="A",
            title_en="A",
            short_description_pt="",
            short_description_en="",
            project_url="https://example.com",
            order=1,
        )
        titles = list(Project.objects.values_list("title_pt", flat=True))
        assert titles == ["A", "B"]


@pytest.mark.unit
@pytest.mark.django_db
class TestAboutMeSingleton:
    def test_save_forces_pk_1(self) -> None:
        a = AboutMe.objects.create(content_pt="pt", content_en="en")
        assert a.pk == 1

    def test_second_save_overwrites_same_row(self) -> None:
        AboutMe.objects.create(content_pt="first", content_en="first-en")
        second = AboutMe(content_pt="second", content_en="second-en")
        second.save()
        assert AboutMe.objects.count() == 1
        assert AboutMe.objects.get().content_pt == "second"

    def test_delete_is_noop(self) -> None:
        about = AboutMe.objects.create(content_pt="x", content_en="y")
        about.delete()
        assert AboutMe.objects.count() == 1

    def test_load_creates_or_returns(self) -> None:
        a1 = AboutMe.load()
        a2 = AboutMe.load()
        assert a1.pk == a2.pk == 1


@pytest.mark.unit
@pytest.mark.django_db
class TestResumeSingleton:
    def test_load_returns_same_instance(self) -> None:
        r1 = Resume.load()
        r2 = Resume.load()
        assert r1.pk == r2.pk == 1

    def test_file_can_be_empty(self) -> None:
        resume = Resume.load()
        assert not resume.file_pt

    def test_file_assignment(self) -> None:
        resume = Resume.load()
        resume.file_pt = SimpleUploadedFile(
            "cv.pdf", b"%PDF-1.4 test", content_type="application/pdf"
        )
        resume.save()
        assert resume.file_pt.name.endswith(".pdf")
