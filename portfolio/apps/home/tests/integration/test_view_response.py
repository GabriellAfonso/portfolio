import pytest
from django.test import Client, TestCase
from django.urls import reverse

from apps.content.models import AboutMe, Project


@pytest.mark.integration
class ViewResponseTest(TestCase):
    def setUp(self) -> None:
        AboutMe.objects.create(
            content_pt="Sobre mim em portugues.",
            content_en="About me in english.",
        )
        Project.objects.create(
            title_pt="Projeto A",
            title_en="Project A",
            short_description_pt="Descricao A",
            short_description_en="Description A",
            project_url="https://example.com/a",
        )

    def test_index_view_renders_correct_content(self) -> None:
        client = Client()
        response = client.get(reverse("home:index"))
        assert response.status_code == 200
        assert b"Gabriel Afonso" in response.content
        assert b"Projeto A" in response.content
        assert "Sobre mim em portugues".encode() in response.content
