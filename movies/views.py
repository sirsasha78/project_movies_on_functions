from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Movie


def movie_list(request: HttpRequest) -> HttpResponse:
    all_movies = Movie.objects.all()
    paginator = Paginator(all_movies, 6)
    page_number = request.GET.get("page", 1)
    movies = paginator.get_page(page_number)

    data = {
        "movies": movies,
        "title": "Главная страница",
    }
    return render(request, "movies/list.html", data)


def movie_detail(request: HttpRequest, slug: str) -> HttpResponse:
    movie = get_object_or_404(Movie, slug=slug)
    data = {
        "movie": movie,
        "title": movie.title,
    }
    return render(request, "movies/detail.html", data)
