from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.files import File
from PIL import Image


def validation_year(value: int):
    """Проверяет, что переданное значение года находится в допустимом диапазоне."""

    current_year = timezone.now().year
    if value < 1888:
        raise ValidationError("Год не может быть меньше 1888")
    if value > current_year + 2:
        raise ValidationError("Год не может быть больше текущего года + 2")


def validate_image_size(value: File):
    """Проверяет размер изображения."""

    filesize = value.size
    if filesize > 5 * 1024 * 1024:
        raise ValidationError("Размер изображения не может превышать 5 МБ.")


def validate_image_with_pillow(value: File):
    """Проверяет, что переданный файл является изображением."""

    try:
        img = Image.open(value)
        img.verify()
        value.seek(0)
    except Exception:
        raise ValidationError("Файл не является валидным изображением.")


IMAGE_VALIDATORS = [
    FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
    validate_image_size,
    validate_image_with_pillow,
]
