from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    first_name = forms.CharField(
        max_length=100,
        label="Имя",
    )
    last_name = forms.CharField(
        max_length=100,
        label="Фамилия",
    )
    username = forms.CharField(max_length=30, label="Имя пользователя")
    email = forms.EmailField(max_length=200, label="Электронная почта")
    password1 = forms.CharField(
        max_length=50, widget=forms.PasswordInput(), label="Пароль"
    )
    password2 = forms.CharField(
        max_length=50, widget=forms.PasswordInput(), label="Подтверждение пароля"
    )

    class Meta:
        """Метакласс формы, определяющий модель и поля, используемые в форме."""

        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    """Форма аутентификации пользователя."""

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
        label="имя пользователя",
    )
    password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Пароль"}),
        label="Пароль",
    )
    remember_me = forms.BooleanField(required=False, label="Запомнить меня")


class UpdateUserForm(forms.ModelForm):
    """Форма для обновления данных пользователя."""

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(),
        label="Имя пользователя",
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(), label="Электронная почта"
    )

    class Meta:
        """Метакласс формы, определяющий модель и поля, используемые в форме."""

        model = get_user_model()
        fields = ["username", "email"]


class UpdateProfileForm(forms.ModelForm):
    """Форма для обновления профиля пользователя."""

    avatar = forms.ImageField(widget=forms.FileInput(), label="Аватар")
    bio = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"rows": 5}), label="Биография"
    )

    class Meta:
        """Метакласс формы, определяющий модель и поля, используемые в форме."""

        model = Profile
        fields = ["avatar", "bio"]
