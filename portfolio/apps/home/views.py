from django.shortcuts import render
from django.http import FileResponse
import os
from django.conf import settings


def index(request):
    return render(request, 'home/index.html')


def curriculo(request):
    PATH = os.path.join(settings.BASE_DIR, 'apps',
                        'home', 'docs', 'curriculo.pdf')
    return FileResponse(open(PATH, 'rb'), content_type='application/pdf')
