from django.test import TestCase
from django.urls import reverse


class URLMappingTest(TestCase):

    def test_webchat_view_url(self):
        url = reverse('webchat:chat')
        self.assertEqual(url, '/webchat/')

    def test_webchat_login_view_url(self):
        url = reverse('webchat:login')
        self.assertEqual(url, '/webchat/login/')

    def test_webchat_singup_view_url(self):
        url = reverse('webchat:singup')
        self.assertEqual(url, '/webchat/singup/')

    def test_webchat_logout_view_url(self):
        url = reverse('webchat:logout')
        self.assertEqual(url, '/webchat/logout/')

    def test_webchat_get_token_view_url(self):
        url = reverse('webchat:get_token')
        self.assertEqual(url, '/webchat/getToken/')
