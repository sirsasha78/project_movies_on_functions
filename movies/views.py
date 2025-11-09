from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from .models import Movie
from .forms import EmailMovieForm, CommentForm, AddMovieForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def movie_list(request: HttpRequest, tag_slug=None) -> HttpResponse:
    """Отображает список фильмов с возможностью фильтрации по тегу и пагинацией."""

    all_movies = Movie.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        all_movies = all_movies.filter(tags=tag)

    paginator = Paginator(all_movies, 6)
    page_number = request.GET.get("page", 1)
    movies = paginator.get_page(page_number)

    data = {
        "movies": movies,
        "title": "Главная страница",
        "tag": tag,
    }
    return render(request, "movies/list.html", data)


def movie_detail(request: HttpRequest, slug: str) -> HttpResponse:
    """Отображает подробную информацию о фильме по его уникальному идентификатору (slug)."""

    movie = get_object_or_404(Movie, slug=slug)
    comments = movie.comments.filter(active=True)
    form = CommentForm()

    similar_movies = movie.tags.similar_objects()[:4]
    data = {
        "movie": movie,
        "title": movie.title,
        "comments": comments,
        "form": form,
        "similar_movies": similar_movies,
    }
    return render(request, "movies/detail.html", data)


def movie_share(request: HttpRequest, movie_id: int) -> HttpResponse:
    """Представление для рекомендации фильма по электронной почте."""

    movie = get_object_or_404(Movie, id=movie_id)
    sent = False

    if request.method == "POST":
        form = EmailMovieForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            movie_url = request.build_absolute_uri(movie.get_absolute_url())
            subject = f"{cd["name"]} рекомендует к просмотру фильм {movie.title}"
            message = (
                f"Посмотреть фильм {movie.title} можно {movie_url}\n\n"
                f"{cd["name"]} {cd["email"]} комментарии: {cd["comments"]}"
            )
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd["to"]])
            sent = True
    else:
        form = EmailMovieForm()
    data = {
        "movie": movie,
        "form": form,
        "sent": sent,
        "title": "Рекомендовать фильм",
    }
    return render(request, "movies/share.html", data)


@require_POST
def movie_comment(request: HttpRequest, movie_id: int) -> HttpResponse:
    """Обрабатывает POST-запрос на добавление комментария к фильму."""

    movie = get_object_or_404(Movie, id=movie_id)
    comment = None

    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.movie = movie
        comment.save()
    data = {
        "title": "Добавить комментарий",
        "movie": movie,
        "form": form,
        "comment": comment,
    }
    return render(request, "movies/comment.html", data)


def add_movie(request: HttpRequest) -> HttpResponse | HttpResponsePermanentRedirect:
    """Обрабатывает добавление нового фильма через форму."""

    if request.method == "POST":
        form = AddMovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("movies:movie_list")
    else:
        form = AddMovieForm()
    data = {
        "title": "Добавление фильма",
        "form": form,
    }
    return render(request, "movies/add_movie.html", data)


def movie_search(request: HttpRequest) -> HttpResponse:
    """Обрабатывает поисковый запрос пользователя и возвращает результаты поиска фильмов."""

    query = request.GET.get("q", "").strip()
    if query:
        search_vector = SearchVector("title", weight="A") + SearchVector(
            "description", weight="B"
        )
        search_query = SearchQuery(query, config="russian")
        results = (
            Movie.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(search=search_query)
            .order_by("-rank")
        )
    else:
        results = []
    data = {
        "title": "Поиск фильма",
        "query": query,
        "results": results,
    }
    return render(request, "movies/search.html", data)
