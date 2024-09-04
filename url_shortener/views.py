from django.shortcuts import render, redirect
from django.views import View
from .models import URL
import random
from webchat.forms import RegisterForm
from django.contrib.auth import logout
import string
from django.contrib import auth, messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm


class ShortenUrl(View):
    @method_decorator(login_required(login_url='url_shortener:login'))
    def get(self, request):
        user = request.user
        user_urls = URL.objects.filter(owner=user)

        context = {'user_urls': user_urls,
                   'base': request.build_absolute_uri(f'/shortener/')}
        return render(
            request,
            'url_shortener/index.html',
            context
        )

    def post(self, request):
        user = request.user

        long_url = request.POST.get('long_url')
        short_url = self.get_random_short_url()

        url = URL(long_url=long_url, short_url=short_url, owner=user)
        url.save()
        full_short_url = request.build_absolute_uri(f'/shortener/{short_url}/')
        user_urls = URL.objects.filter(owner=user)

        context = {'user_urls': user_urls,
                   'base': request.build_absolute_uri(f'/shortener/'),
                   'short_url': full_short_url}

        return render(request, 'url_shortener/index.html', context)

    def get_random_short_url(self):
        while True:
            short_url = ''.join(random.choices(
                string.ascii_letters + string.digits, k=6))
            if not URL.objects.filter(short_url=short_url).exists():
                return short_url


def redirect_view(request, short_url):
    url = URL.objects.get(short_url=short_url)
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
        form = RegisterForm()
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
        form = RegisterForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
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
