from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
import random
import string
from apps.picpay.models import Account
from rolepermissions.roles import assign_role
from django.http import HttpResponseBadRequest
from django.http import FileResponse
import os
from django.conf import settings


def index(request):

    context = {

    }

    return render(
        request,
        'home/index.html',
        context,
    )


def guest_login(request, app_name):
    username = "guest_" + \
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    user = User.objects.create_user(username=username)
    user.set_unusable_password()
    user.save()
    login(request, user)

    if app_name == "webchat":
        return redirect("webchat:chat")
    elif app_name == "url_shortener":
        return redirect("url_shortener:shorten-url")
    elif app_name == "picpay":
        Account.objects.create(
            user=user,
            complete_name="Convidado PicPay",
            email=f"{username}@guest.com",
            document="00000000000",
            document_type="cpf",
            sex="M",
            account_type="personal",
            balance=100
        )
        assign_role(user, 'personal')
        return redirect("picpay:profile")
    else:
        return HttpResponseBadRequest("App inválido")


def curriculo(request):
    PATH = os.path.join(settings.BASE_DIR, 'apps', 'home',
                        'static', 'home', 'docs', 'curriculo.pdf')
    return FileResponse(open(PATH, 'rb'), content_type='application/pdf')
