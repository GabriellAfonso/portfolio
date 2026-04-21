import pytest
from django.test import TestCase
from django.urls import reverse


@pytest.mark.unit
class UrlPathTest(TestCase):
    def test_index_url_path(self) -> None:
        assert reverse("home:index") == "/"
