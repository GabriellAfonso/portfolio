from django.shortcuts import render
from django.views import View
from .models import Music


class Home(View):

    def get(self, request):
        return render(request, 'igreja/index.html')


class Tables(View):

    def get(self, request):
        return render(request, 'igreja/tables.html')


class RegisterSundays(View):

    def get(self, request):
        notes = ["A", "A#", "Bb", "B", "C", "C#", "Db", "D",
                 "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab"]
        musics = Music.objects.all().order_by('title')
        context = {
            'notes': notes,
            'musics': musics,
        }
        return render(request, 'igreja/register_sundays.html', context)

    # def post(self, request):
    #     # Capturando dados do formulário
    #     date = request.POST.get('date')
    #     musics = [
    #         (request.POST.get('first_music'), request.POST.get('tune_first_music')),
    #         (request.POST.get('second_music'),
    #          request.POST.get('tune_second_music')),
    #         (request.POST.get('third_music'), request.POST.get('tune_third_music')),
    #         (request.POST.get('fourth_music'),
    #          request.POST.get('tune_fourth_music')),
    #     ]

    #     # Salvando músicas no banco de dados com a mesma data
    #     for name, tone in musics:
    #         if name:
    #             music_name = name.strip().upper()
    #             Music.objects.create(
    #                 name=music_name, date=date, tone=tone or None)

    #     return redirect('culto_musicas:home')
