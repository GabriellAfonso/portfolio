from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.views import View
from .models import URL
import random
from django.contrib.auth import logout
import string
from django.contrib import auth, messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from apps.webchat.views.views import create_generic_account
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from core.forms import BaseRegisterForm


class ShortenUrl(View):
    @method_decorator(login_required(login_url='url_shortener:login'))
    def get(self, request):
        user = request.user
        user_urls = URL.objects.filter(owner=user)
        base_url = self.get_base_url(request)

        context = {'user_urls': user_urls,
                   'base': base_url}

        return render(
            request,
            'url_shortener/index.html',
            context
        )

    def post(self, request):
        user = request.user
        base_url = self.get_base_url(request)
        long_url = request.POST.get('long_url')
        short_url = self.get_random_short_url()
        validator = URLValidator()

        try:
            validator(long_url)
        except ValidationError:
            messages.error(
                request, 'URL inválida. Por favor, insira uma URL válida.')
            return redirect('url_shortener:shorten-url')

        url = URL(long_url=long_url, short_url=short_url, owner=user)
        url.save()

        user_urls = URL.objects.filter(owner=user)

        context = {'user_urls': user_urls,
                   'base': base_url,
                   'shortened_url': f'{base_url['full']}s/{short_url}'}

        return render(request, 'url_shortener/index.html', context)

    def get_random_short_url(self):
        while True:
            short_url = ''.join(random.choices(
                string.ascii_letters + string.digits, k=6))
            if not URL.objects.filter(short_url=short_url).exists():
                return short_url

    def get_base_url(self, request):
        scheme = request.scheme
        host = request.get_host()
        url = {'full': f'{scheme}://{host}/',
               'short': f'{host}/'}
        return url


def redirect_view(request, short_url):
    url = get_object_or_404(URL, short_url=short_url)
    return redirect(url.long_url)


class Login(View):

    def get(self, request):
        form = AuthenticationForm(request)
        context = {'form': form}

        return render(
            request,
            'url_shortener/login.html',
            context,
        )

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('url_shortener:shorten-url')

        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('url_shortener:login')


class SingUp(View):

    def get(self, request):
        form = BaseRegisterForm()
        created_account = False
        context = {
            'form': form,
            'created_account': created_account,
        }

        return render(
            request,
            'url_shortener/singup.html',
            context,
        )

    def post(self, request):
        form = BaseRegisterForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            create_generic_account(user)
            created_account = True
            context['created_account'] = created_account

        return render(
            request,
            'url_shortener/singup.html',
            context,
        )


class Logout(View):

    @method_decorator(login_required(login_url='url_shortener:login'))
    def get(self, request):
        logout(request)
        return redirect('url_shortener:login')
