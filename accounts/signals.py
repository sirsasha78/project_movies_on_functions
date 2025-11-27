from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from PIL import Image
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender: type, instance: User, created: bool, **kwargs) -> None:
    """Создаёт профиль автоматически при создании пользователя."""

    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def resize_avatar(sender: type, instance: Profile, created: bool, **kwargs) -> None:
    """Сжимает аватар до 100x100 пикселей, если он был загружен."""

    if instance.avatar:
        img = Image.open(instance.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(instance.avatar.path)
