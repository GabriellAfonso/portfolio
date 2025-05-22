from django.test import TestCase
from django.urls import reverse, resolve


class UrlPathTest(TestCase):

    def test_index_url_path(self):
        assert reverse("home:index") == "/"

    def test_curriculo_url_path(self):
        assert reverse("home:curriculo") == "/curriculo/"
