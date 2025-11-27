from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import QuerySet
from .models import Movie
from .forms import EmailMovieForm, CommentForm, AddMovieForm, MovieUpdateForm
from typing import Any


class MovieList(ListView):
    """Класс-представление для отображения списка фильмов.
    Отображает фильмы на странице с поддержкой пагинации и фильтрации по тегам."""

    template_name = "movies/list.html"
    context_object_name = "movies"
    paginate_by = 6
    tag = None
    total_movies = Movie.objects.count()

    def get_queryset(self) -> QuerySet[Movie]:
        """Возвращает отфильтрованный QuerySet фильмов.
        Если в URL передан слаг тега, возвращает фильмы, отмеченные этим тегом.
        Иначе возвращает все фильмы."""

        tag_slug = self.kwargs.get("tag_slug")
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = Movie.objects.prefetch_related("tags").filter(
                tags__slug=self.tag.slug
            )
        else:
            queryset = Movie.objects.prefetch_related("tags").all()
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Добавляет дополнительные данные в контекст шаблона."""

        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        context["total_movies"] = self.total_movies
        context["title"] = (
            f"Фильмы с тэгом: {self.tag.slug}" if self.tag else "Главная страница"
        )
        return context


class MovieDetailView(DetailView):
    """Представление для отображения детальной информации о фильме.
    Отображает страницу с подробной информацией о выбранном фильме,
    включая форму добавления комментария, список активных комментариев
    и похожие фильмы на основе тегов."""

    model = Movie
    template_name = "movies/detail.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Добавляет дополнительные данные в контекст шаблона."""

        context = super().get_context_data(**kwargs)
        context["title"] = context["movie"].title
        context["form"] = CommentForm()
        context["comments"] = context["movie"].comments.filter(active=True)
        context["similar_movies"] = context["movie"].tags.similar_objects()[:4]
        return context


class MovieShare(FormView):
    """Класс-представление для отправки рекомендации фильма по электронной почте."""

    form_class = EmailMovieForm
    template_name = "movies/share.html"

    def dispatch(
        self, request: HttpRequest, movie_id: int, *args, **kwargs
    ) -> HttpResponse:
        """Инициализирует объект фильма и его абсолютную ссылку перед обработкой запроса."""

        self.movie = get_object_or_404(Movie, id=movie_id)
        self.movie_url = request.build_absolute_uri(self.movie.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        """Возвращает URL-адрес для перенаправления после успешной отправки формы."""

        return self.movie.get_absolute_url()

    def form_valid(self, form: EmailMovieForm) -> HttpResponse:
        """Обрабатывает валидную форму, отправляя email с рекомендацией фильма."""

        cd = form.cleaned_data
        subject = f"{cd['name']} рекомендует к просмотру фильм {self.movie.title}"
        message = (
            f"Посмотреть фильм {self.movie.title} можно {self.movie_url}\n\n"
            f"{cd['name']} {cd['email']} комментарии: {cd['comments']}"
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [cd["to"]])
        messages.success(self.request, f"Письмо было успешно отправлено {cd["to"]}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Добавляет в контекст шаблона объект фильма и заголовок страницы."""

        context = super().get_context_data(**kwargs)
        context["movie"] = self.movie
        context["title"] = "Рекомендовать фильм"
        return context


class MovieComment(CreateView):
    """Представление для добавления комментария к фильму."""

    form_class = CommentForm
    template_name = "movies/comment.html"

    def dispatch(
        self, request: HttpRequest, movie_id: int, *args, **kwargs
    ) -> HttpResponse:
        """Инициализирует объект фильма перед обработкой запроса."""

        self.movie = get_object_or_404(Movie, id=movie_id)
        self.comment = None
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: CommentForm) -> HttpResponse:
        """Обрабатывает валидную форму, сохраняя комментарий."""

        self.comment = form.save(commit=False)
        self.comment.movie = self.movie
        return super().form_valid(form)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Добавляет в контекст шаблона объект фильма и комментарий."""

        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить комментарий"
        context["movie"] = self.movie
        context["comment"] = self.comment
        return context

    def get_success_url(self) -> str:
        """Возвращает URL-адрес для перенаправления после успешного добавления комментария."""

        return self.movie.get_absolute_url()


class AddMovie(LoginRequiredMixin, CreateView):
    """Представление для добавления нового фильма."""

    form_class = AddMovieForm
    template_name = "movies/add_movie.html"
    success_url = reverse_lazy("movies:movie_list")
    login_url = "movies:movie_list"
    extra_context = {
        "title": "Добавление фильма",
    }


class MovieSearch(ListView):
    """Представление для поиска фильмов."""

    template_name = "movies/search.html"
    context_object_name = "results"

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Обрабатывает запрос пользователя и сохраняет поисковый запрос."""

        self.query = request.GET.get("q", "").strip()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Movie]:
        """Возвращает набор результатов поиска фильмов."""

        if self.query:
            search_vector = SearchVector("title", weight="A") + SearchVector(
                "description", weight="B"
            )
            search_query = SearchQuery(self.query, config="russian")
            return (
                Movie.objects.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(search=search_query)
                .order_by("-rank")
            )
        return Movie.objects.none()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Добавляет дополнительные данные в контекст шаблона."""

        context = super().get_context_data(**kwargs)
        context["title"] = "Поиск фильма"
        context["query"] = self.query
        return context


class MovieUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Представление для обновления информации о фильме."""

    model = Movie
    form_class = MovieUpdateForm
    template_name = "movies/movie_update.html"
    context_object_name = "movie"
    login_url = "movies:movie_list"
    success_message = "Фильм был успешно обновлен!"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Возвращает контекст данных для шаблона."""

        context = super().get_context_data(**kwargs)
        context["title"] = f"Обновление фильма: {self.object.title}"
        return context
