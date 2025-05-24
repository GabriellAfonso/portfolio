from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import auth, messages
from apps.picpay.forms import PicPayRegisterForm
from apps.picpay.models import PicPayAccount, Transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.timezone import now
from django.http import JsonResponse
from apps.picpay.services.register_picpay_user import PicPayRegistrationService
from core.forms import EmailAuthenticationForm
from apps.picpay.utils import get_first_and_last_name
from apps.picpay.services.profile_service import get_last_transactions


class Login(View):

    def get(self, request):
        form = EmailAuthenticationForm(request=request)
        context = {'form': form, }
        return render(request, 'picpay/login.html', context)

    def post(self, request):
        form = EmailAuthenticationForm(data=request.POST, request=request)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('picpay:profile')

        return render(request, 'picpay/login.html', {'form': form})


class Register(View):

    def get(self, request):
        form = PicPayRegisterForm()
        created_account = False
        context = {
            'form': form,
            'created_account': created_account,
        }
        return render(request, 'picpay/register.html', context)

    def post(self, request):
        form = PicPayRegisterForm(request.POST)

        if form.is_valid():
            PicPayRegistrationService(form.cleaned_data).register()

            return redirect('picpay:login')
        return render(request, 'picpay/register.html', {'form': form})


class YourProfile(View):

    @method_decorator(login_required(login_url='picpay:login'))
    def get(self, request):
        user = request.user
        account = PicPayAccount.objects.get(user=user.id)
        display_name = get_first_and_last_name(account.complete_name)
        context = {'display_name': display_name,
                   'balance': account.balance,
                   'sex': account.sex,
                   'last_transactions': get_last_transactions(account)
                   }
        return render(request, 'picpay/profile.html', context)


class Logout(View):

    @method_decorator(login_required(login_url='picpay:login'))
    def get(self, request):
        logout(request)
        return redirect('picpay:login')


@login_required(login_url='picpay:login')
def start_transaction(request):
    document = request.GET.get('document')
    print(document)
    if document:
        try:
            account = PicPayAccount.objects.get(document=document)
            data = {
                'name': account.complete_name,
            }
            return JsonResponse(data)
        except PicPayAccount.DoesNotExist:
            return JsonResponse({'error': 'Account not found'}, status=404)
    else:
        return JsonResponse({'error': 'No document provided'}, status=400)
