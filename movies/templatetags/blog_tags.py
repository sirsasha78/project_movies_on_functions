from django import template
from movies.models import Movie
from django.db.models.query import QuerySet
from django.db.models import Count


register = template.Library()


@register.simple_tag
def total_movies() -> int:
    """Вывод общего количества фильмов."""

    return Movie.objects.count()


@register.inclusion_tag("movies/top_movies.html")
def show_top_movies(count=5) -> dict[str, QuerySet[Movie]]:
    """Вывод топовых фильмов."""

    top_movies = Movie.objects.order_by("-rating")[:count]
    return {"top_movies": top_movies}


@register.simple_tag
def get_most_commented_movies(count=5) -> QuerySet[Movie]:
    """Вывод фильмов с наибольшим количеством комментариев."""

    return (
        Movie.objects.annotate(total_comments=Count("comments"))
        .exclude(total_comments=0)
        .order_by("-total_comments")[:count]
    )
