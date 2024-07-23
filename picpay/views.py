from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import auth, messages
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


class Login(View):

    def get(self, request):
        form = AuthenticationForm(request)
        context = {'form': form, }
        return render(request, 'picpay/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('picpay:profile')

        else:
            print(form.errors)
            messages.error(request, 'E-mail ou senha inválidos.')
            return redirect('picpay:login')


class Register(View):

    def get(self, request):
        form = RegisterForm()
        created_account = False
        context = {
            'form': form,
            'created_account': created_account,
        }
        return render(request, 'picpay/register.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            print('foi salvo')
            return redirect('picpay:login')

        return render(request, 'picpay/register.html', {'form': form})


class Profile(View):

    @method_decorator(login_required(login_url='picpay:login'))
    def get(self, request):
        return render(request, 'picpay/profile.html')


class Logout(View):

    @method_decorator(login_required(login_url='picpay:login'))
    def get(self, request):
        logout(request)
        return redirect('picpay:login')
