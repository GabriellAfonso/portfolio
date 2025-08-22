import pytest
from django.test import TestCase, Client
from django.urls import reverse


@pytest.mark.integration
class ViewResponseTest(TestCase):

    def test_index_view_renders_correct_content(self):
        client = Client()
        response = client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Gabriel Afonso", response.content)

    def test_curriculo_view_renders_correct_content(self):
        client = Client()
        response = client.get(reverse("home:curriculo"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
