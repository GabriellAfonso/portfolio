from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from webchat.forms import RegisterForm
from django.contrib import auth, messages
from django.contrib.auth import logout
from ..models import Profile
from django.http import JsonResponse
from rest_framework.authtoken.models import Token


@login_required(login_url='webchat:login')
def webchat(request):

    if request.user.is_authenticated:
        user = request.user

        # Verifica se o usuario ja existe
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        if not profile:
            profile = Profile(user=user)
            profile.save()

    profile = Profile.objects.get(user=user)

    context = {
        'profile': profile,
    }

    return render(
        request,
        'webchat/webchat.html',
        context,
    )


def login(request):

    form = AuthenticationForm(request)
    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('webchat:chat')

        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            return redirect('webchat:login')

    else:
        form = AuthenticationForm(request)

    context = {
        'form': form,
    }

    return render(
        request,
        'webchat/login.html',
        context,
    )


def singup(request):

    form = RegisterForm()
    created_account = False

    if request.method == 'POST':
        print(RegisterForm())
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            created_account = True
            context = {'created_account': created_account, }

            return render(
                request,
                'webchat/singup.html',
                context,
            )

        else:
            pass

    context = {
        'form': form,
        'created_account': created_account,
    }

    return render(
        request,
        'webchat/singup.html',
        context,
    )


@login_required(login_url='webchat:login')
def get_token(request):
    user = request.user
    token, created = Token.objects.get_or_create(user=user)
    data = {'token': str(token)}

    return JsonResponse(data)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('webchat:login')
