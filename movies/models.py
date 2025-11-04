from django.core.validators import (
    FileExtensionValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from unidecode import unidecode
from typing import Any


def validation_year(value: int):
    """Проверяет, что переданное значение года находится в допустимом диапазоне."""

    current_year = timezone.now().year
    if value < 1888:
        raise ValidationError("Год не может быть меньше 1888")
    if value > current_year + 2:
        raise ValidationError("Год не может быть больше текущего года + 2")


class AutoSlugMixin(models.Model):
    """Абстрактный миксин для автоматического генерирования уникального slug-поля модели.
    Подклассы должны реализовать метод `get_field_for_slug`, возвращающий имя атрибута модели,
    значение которого используется для генерации slug."""

    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        abstract = True

    def get_field_for_slug(self) -> Any:
        """Абстрактный метод, который должен быть переопределен в подклассе."""

        raise NotImplementedError("Подкласс обязан определить метод get_field_for_slug")

    def generate_slug(self) -> str:
        """Генерирует уникальный slug на основе значения поля, указанного в `get_field_for_slug`."""

        field_name = self.get_field_for_slug()
        value_to_slug = getattr(self, field_name)
        unique_slug = slugify(unidecode(value_to_slug), allow_unicode=False)
        counter = 1

        while self.__class__.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{unique_slug}-{counter}"
            counter += 1
        return unique_slug

    def save(self, *args, **kwargs):
        """Сохраняет модель, генерируя slug, если он не установлен."""

        if not self.slug:
            self.slug = self.generate_slug()
        return super().save(*args, **kwargs)


class Genre(AutoSlugMixin):
    """Модель, представляющая жанр в системе."""

    name = models.CharField(max_length=100, verbose_name="Жанр")

    def __str__(self) -> str:
        """Возвращает строковое представление объекта жанра."""

        return self.name

    def get_field_for_slug(self) -> str:
        """Возвращает имя поля, используемого для генерации слага."""

        return "name"

    class Meta:
        """Класс метаданных для настройки модели Genre."""

        db_table = "genre"
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Director(AutoSlugMixin):
    """Модель режиссера для хранения информации о режиссерах."""

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")

    def __str__(self) -> str:
        """Возвращает строковое представление объекта в формате 'Фамилия Имя'."""

        return f"{self.last_name} {self.first_name}"

    def get_field_for_slug(self) -> str:
        """Возвращает имя поля, используемого для генерации slug."""

        return "last_name"

    class Meta:
        """Класс Meta содержит метаданные модели."""

        db_table = "director"
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"


class Movie(AutoSlugMixin):
    """Модель для представления информации о фильме."""

    title = models.CharField(max_length=255, verbose_name="Название фильма")
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

    def get_field_for_slug(self) -> str:
        """Возвращает поле модели, используемое для генерации slug."""

        return "title"

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
