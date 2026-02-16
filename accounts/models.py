from django.db import models
from django.contrib.auth.models import User
from services.validators import IMAGE_VALIDATORS


class Profile(models.Model):
    """Модель профиля пользователя.
    Связывает пользователя с его дополнительной информацией: аватаром и биографией.
    Каждый пользователь может иметь только один профиль."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    avatar = models.ImageField(
        default="default.jpg",
        validators=IMAGE_VALIDATORS,
        upload_to="profile_images/%Y/%m/%d/",
        verbose_name="Аватар",
    )
    bio = models.TextField(blank=True, verbose_name="Биография")

    def __str__(self) -> str:
        """Возвращает строковое представление профиля."""

        return self.user.username

    class Meta:
        """Метакласс для настройки поведения модели."""

        db_table = "profile"
        ordering = ("user",)
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
