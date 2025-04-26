from django.shortcuts import render


def index(request):

    context = {

    }

    return render(
        request,
        'portifolio/index.html',
        context,
    )
