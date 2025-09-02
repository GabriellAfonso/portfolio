from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
import random
import string
from apps.picpay.models import PicPayAccount
from rolepermissions.roles import assign_role
from django.http import HttpResponseBadRequest
from django.http import FileResponse
import os
from django.conf import settings
from apps.webchat.views.views import create_generic_account


def index(request):
    return render(request, 'home/index.html')


def guest_login(request, app_name):
    username = "guest_" + \
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    user = User.objects.create_user(username=username)
    print('Usuário guest criado:', user.id, user.username)
    user.set_unusable_password()
    user.save()
    create_generic_account(user)
    assign_role(user, 'personal')

    if app_name == "webchat":
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect("webchat:chat")
    elif app_name == "url_shortener":
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect("url_shortener:shorten-url")
    elif app_name == "picpay":
        login(request, user, backend='core.auth_backend.EmailBackend')
        return redirect("picpay:profile")
    else:
        return HttpResponseBadRequest("App inválido")


def curriculo(request):
    PATH = os.path.join(settings.BASE_DIR, 'apps',
                        'home', 'docs', 'curriculo.pdf')
    return FileResponse(open(PATH, 'rb'), content_type='application/pdf')
