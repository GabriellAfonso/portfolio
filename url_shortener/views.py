from django.shortcuts import render, redirect
from django.views import View
from .models import URL
import random
import string


class ShortenUrl(View):

    def get(self, request):
        return render(
            request,
            'url_shortener/index.html'
        )

    def post(self, request):
        long_url = request.POST.get('long_url')
        short_url = self.get_random_short_url()

        url = URL(long_url=long_url, short_url=short_url)
        url.save()

        return render(request, 'url_shortener/index.html', {'short_url': short_url})

    def get_random_short_url(self):
        while True:
            short_url = ''.join(random.choices(
                string.ascii_letters + string.digits, k=6))
            if not URL.objects.filter(short_url=short_url).exists():
                return short_url


def redirect_view(request, short_url):
    url = URL.objects.get(short_url=short_url)
    return redirect(url.long_url)
