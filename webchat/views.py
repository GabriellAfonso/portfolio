from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth, messages

@login_required(login_url='webchat:login')
def webchat(request):

    context = {}

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
            auth.login(request,user)
            return redirect('webchat:chat')

        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            print('Usuário ou senha inválidos.')
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

def register(request):

    context = {}

    return render(
        request,
        'webchat/register.html',
        context,
    )
