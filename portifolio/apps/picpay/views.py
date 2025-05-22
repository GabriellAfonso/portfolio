from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import auth, messages
from apps.picpay.forms import PicPayRegisterForm
from apps.picpay.models import PicPayAccount, Transaction
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_permission
from django.utils.timezone import now
from django.http import JsonResponse
from apps.picpay.services.register_picpay_user import PicPayRegistrationService


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
        username = self.get_first_and_last_name(account.complete_name)
        context = {'username': username,
                   'balance': account.balance,
                   'sex': account.sex,
                   'last_transactions': self.get_last_transactions(account)
                   }
        return render(request, 'picpay/profile.html', context)

    def get_first_and_last_name(self, full_name):
        parts = full_name.split()

        first_name = parts[0].capitalize()

        if len(parts) > 1:
            last_name = parts[-1].capitalize()
            return f"{first_name} {last_name}"
        else:
            return first_name

    def get_last_transactions(self, account):
        last_transactions = Transaction.objects.filter(
            Q(sender=account) | Q(receiver=account)
        ).order_by('-created_at')[:3]

        processed_transactions = []
        for transaction in last_transactions:

            if transaction.sender_id == account.id:
                action = "Enviou"
                counterpart = transaction.receiver.complete_name
            else:
                action = "Recebeu"
                counterpart = transaction.sender.complete_name

            time_elapsed = now() - transaction.created_at
            days_ago = time_elapsed.days
            if days_ago == 0:
                time_str = "Hoje"
            elif days_ago == 1:
                time_str = "Ontem"
            else:
                time_str = f"{days_ago} dias atrás"

            processed_transactions.append({
                'action': action,
                'time': time_str,
                'value': transaction.value,
                'counterpart': self.get_first_and_last_name(counterpart)
            })

        return processed_transactions


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
