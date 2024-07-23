from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import auth, messages
from .forms import RegisterForm
from .models import Profile
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


class YourProfile(View):

    @method_decorator(login_required(login_url='picpay:login'))
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        username = self.get_first_and_last_name(profile.complete_name)
        context = {'username': username,
                   'balance': profile.balance,
                   'sex': profile.sex,
                   }
        print(context)
        return render(request, 'picpay/profile.html', context)

    def get_first_and_last_name(self, full_name):
        parts = full_name.split()

        first_name = parts[0].capitalize()
        last_name = parts[-1].capitalize()
        return f"{first_name} {last_name}"


class Logout(View):

    @method_decorator(login_required(login_url='picpay:login'))
    def get(self, request):
        logout(request)
        return redirect('picpay:login')
