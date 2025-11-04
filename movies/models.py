from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse
from autoslug import AutoSlugField


def validation_year(value: int):
    """Проверяет, что переданное значение года находится в допустимом диапазоне."""

    current_year = timezone.now().year
    if value < 1888:
        raise ValidationError("Год не может быть меньше 1888")
    if value > current_year + 2:
        raise ValidationError("Год не может быть больше текущего года + 2")


class Genre(models.Model):
    """Модель, представляющая жанр в системе."""

    name = models.CharField(max_length=100, verbose_name="Жанр")
    slug = AutoSlugField(
        populate_from="name", max_length=255, unique=True, db_index=True
    )

    def __str__(self) -> str:
        """Возвращает строковое представление объекта жанра."""

        return self.name

    class Meta:
        """Класс метаданных для настройки модели Genre."""

        db_table = "genre"
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Director(models.Model):
    """Модель режиссера для хранения информации о режиссерах."""

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    slug = AutoSlugField(
        populate_from="last_name",
        unique_with="first_name",
        max_length=255,
        unique=True,
        db_index=True,
    )

    def __str__(self) -> str:
        """Возвращает строковое представление объекта в формате 'Фамилия Имя'."""

        return f"{self.last_name} {self.first_name}"

    class Meta:
        """Класс Meta содержит метаданные модели."""

        db_table = "director"
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"


class Movie(models.Model):
    """Модель для представления информации о фильме."""

    title = models.CharField(max_length=255, verbose_name="Название фильма")
    slug = AutoSlugField(
        populate_from="title", max_length=255, unique=True, db_index=True
    )
    description = models.TextField(verbose_name="Описание фильма")
    trailer = models.URLField(blank=True, verbose_name="Ссылка на трэйлер")
    year = models.PositiveIntegerField(
        validators=[
            validation_year,
        ],
        verbose_name="Год выхода",
    )
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name="Рэйтинг",
    )
    genre = models.ForeignKey(
        Genre,
        null=True,
        on_delete=models.SET_NULL,
        related_name="genre_movies",
        verbose_name="Жанр",
    )
    director = models.ForeignKey(
        Director,
        null=True,
        on_delete=models.SET_NULL,
        related_name="director_movies",
        verbose_name="Режиссер",
    )
    photo = models.ImageField(
        upload_to="movies/",
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
        blank=True,
        null=True,
        default=None,
        verbose_name="Изображение",
    )

    def __str__(self) -> str:
        """Возвращает строковое представление объекта класса."""

        return self.title

    class Meta:
        """Дополнительные параметры модели."""

        db_table = "movie"
        ordering = ["-rating"]
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def get_absolute_url(self) -> str:
        """Возвращает URL-адрес для детального просмотра фильма."""

        return reverse("movies:movie_detail", args=[self.slug])


class Comment(models.Model):
    """Модель для хранения комментариев к фильмам."""

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Фильм",
    )
    name = models.CharField(max_length=80, verbose_name="Имя")
    email = models.EmailField(verbose_name="Электронная почта")
    body = models.TextField(verbose_name="Комментарий")
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания комментария"
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Дата обновления комментария"
    )
    active = models.BooleanField(default=True, verbose_name="Активность комментария")

    class Meta:
        """Метакласс для настройки поведения модели."""

        db_table = "comment"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["created"]
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self) -> str:
        """Возвращает строковое представление комментария."""

        return f"Комментарий {self.name} фильма {self.movie}"
