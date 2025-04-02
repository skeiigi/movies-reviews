from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movies


def index(request):
    return render(request, "index.html", {"name": 'neithiri'})


def movies(request):
    movie = Movies.objects.all

    return render(request, "movies_page.html", {'movie': movie})
