from django.contrib.sitemaps import Sitemap
from .models import Movie
from django.db.models.query import QuerySet


class MovieSitemap(Sitemap):
    """Сайтмап фильмов."""

    changefreq = "weekly"
    priority = 0.9

    def items(self) -> QuerySet[Movie]:
        """Вывод всех фильмов."""

        return Movie.objects.all()
