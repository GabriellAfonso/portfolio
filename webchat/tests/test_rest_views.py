from django.test import TestCase
from django.urls import reverse


class ApiUrlMappingTest(TestCase):

    def test_webchat_api_profile_url(self):
        url = reverse('webchat:user_profile', kwargs={'pk': 1})

        self.assertEqual(url, '/webchat/api/profile/1/')
