from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movies
from .forms import MovieForm


def index(request):
    return render(request, "index.html", {"name": 'neithiri'})


def movies(request):
    # Получаем все фильмы из базы данных
    movies_list = Movies.objects.all

    if request.method == "POST":
        # Если запрос POST, создаем форму с данными из запроса
        form = MovieForm(request.POST, request.FILES)  # Добавляем request.FILES для загрузки изображений
        if form.is_valid():
            # Если форма валидна, сохраняем данные и перенаправляем на страницу
            form.save()
            return render(request, "movies_page.html", {'form': form, 'movies': movies_list})
    else:
        # Если запрос GET, создаем пустую форму
        form = MovieForm()

    # Передаем форму и список фильмов в контекст
    return render(request, "movies_page.html", {'form': form, 'movies': movies_list})
