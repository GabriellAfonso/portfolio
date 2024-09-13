import re
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.db.models import Count
from django.db.models import Q
from .models import Music, Played


class Home(View):

    def get(self, request):
        return render(request, 'igreja/index.html')


class Tables(View):

    def get(self, request):
        last_songs = Played.objects.all().order_by('-date', 'position')

        top_songs = Played.objects.values('music__title').annotate(
            play_count=Count('music')).order_by('-play_count')

        top_tones = Played.objects.values('tone').annotate(
            tone_count=Count('tone')).order_by('-tone_count')

        print(top_songs)
        context = {
            'last_songs': last_songs,
            'top_songs': top_songs,
            'top_tones': top_tones,
        }

        return render(request, 'igreja/tables.html', context)


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

    def post(self, request):
        # Capturando dados do formulário
        date = request.POST.get('date')
        musics = [
            (request.POST.get('first_music'),
             request.POST.get('tone_first_music'), 1),
            (request.POST.get('second_music'),
             request.POST.get('tone_second_music'), 2),
            (request.POST.get('third_music'),
             request.POST.get('tone_third_music'), 3),
            (request.POST.get('fourth_music'),
             request.POST.get('tone_fourth_music'), 4),
        ]

        print(musics)
        # Salvando músicas no banco de dados com a mesma data
        for music, tone, position in musics:
            if music:
                cleaned_name,  artist = self.clean_music_title(music)
                try:
                    music = Music.objects.get(
                        title=cleaned_name,  artist=artist)
                    music_id = music.id
                except Music.DoesNotExist:
                    # Caso a música não seja encontrada, continue com o próximo item
                    music_id = None
                    # Opcional: você pode adicionar uma mensagem de erro aqui

                if music_id:
                    Played.objects.create(
                        music_id=music_id, date=date, tone=tone, position=position
                    )
        return redirect('igreja:tabela')

    def clean_music_title(self, title):
        match = re.match(r'^(.*?)\s*\[(.*?)\]\s*$', title)
        if match:
            cleaned_title = match.group(1).strip()
            artist = match.group(2).strip()
            return [cleaned_title,  artist]

        return [title.strip(), '']


class FindMusic(View):
    def get(self, request):
        query = request.GET.get('query')
        if query:
            musics = Music.objects.filter(
                Q(title__icontains=query) | Q(artist__icontains=query)
            )
        else:
            musics = Music.objects.all()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Se a requisição for AJAX, retorna um JSON
            music_data = list(musics.values('title', 'artist'))
            return JsonResponse({'musics': music_data})

        context = {
            'musics': musics,
        }
        return render(request, 'igreja/search.html', context)
