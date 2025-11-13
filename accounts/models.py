from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from PIL import Image
from services.validators import validate_image_size, validate_image_with_pillow


class Profile(models.Model):
    """Модель профиля пользователя.
    Связывает пользователя с его дополнительной информацией: аватаром и биографией.
    Каждый пользователь может иметь только один профиль."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    avatar = models.ImageField(
        default="default.jpg",
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
            validate_image_with_pillow,
        ],
        upload_to="profile_images",
        verbose_name="Аватар",
    )
    bio = models.TextField(blank=True, verbose_name="Биография")

    def __str__(self) -> str:
        """Возвращает строковое представление профиля."""

        return self.user.username

    class Meta:
        """Метакласс для настройки поведения модели."""

        db_table = "profile"
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def save(self, *args, **kwargs):
        """Сохраняет профиль и сжимает аватар до размера 100x100 пикселей."""

        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
