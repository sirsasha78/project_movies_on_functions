from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Movie


def movie_list(request: HttpRequest) -> HttpResponse:
    movies = Movie.objects.all()
    data = {
        "movies": movies,
        "title": "Главная страница",
    }
    return render(request, "movies/list.html", data)


def movie_detail(request: HttpRequest, id: int) -> HttpResponse:
    movie = get_object_or_404(Movie, id=id)
    data = {
        "movie": movie,
        "title": movie.title,
    }
    return render(request, "movies/detail.html", data)
