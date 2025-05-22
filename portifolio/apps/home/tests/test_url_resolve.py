from django.test import TestCase
from django.urls import reverse, resolve
from apps.home import views


class UrlResolveTest(TestCase):

    def test_index_url_resolves_to_correct_view(self):
        assert resolve("/").func == views.index

    def test_curriculo_url_resolves_to_correct_view(self):
        assert resolve("/curriculo/").func == views.curriculo
