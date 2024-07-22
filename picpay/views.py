from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .forms import RegisterForm


class Login(View):

    def get(self, request):
        return render(request, 'picpay/login.html')


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
        else:
            print('nao foi')
            print(form.errors)  # Adiciona isso para exibir os erros no console
        return render(request, 'picpay/register.html', {'form': form})


class Profile(View):

    def get(self, request):
        return render(request, 'picpay/profile.html')
