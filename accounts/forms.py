from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
from services.validators import IMAGE_VALIDATORS
from .models import Profile


class SignUpForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    first_name = forms.CharField(
        max_length=100,
        label="Имя",
        widget=forms.TextInput(
            attrs={"class": "form-control mb-1", "placeholder": "Введите имя"}
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        label="Фамилия",
        widget=forms.TextInput(
            attrs={"class": "form-control mb-1", "placeholder": "Введите фамилию"}
        ),
    )
    username = forms.CharField(
        max_length=30,
        label="Имя пользователя",
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-1",
                "placeholder": "Введите имя пользователя",
            }
        ),
    )
    email = forms.EmailField(
        max_length=200,
        label="Электронная почта",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-1",
                "placeholder": "Введите электронную почту",
            }
        ),
    )
    password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-1", "placeholder": "Введите пароль"}
        ),
        label="Пароль",
    )
    password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-1", "placeholder": "Подтвердите пароль"}
        ),
        label="Подтверждение пароля",
    )
    recaptcha = ReCaptchaField()

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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой email уже используется в системе")
        return email


class LoginForm(AuthenticationForm):
    """Форма аутентификации пользователя."""

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-1", "placeholder": "Имя пользователя"}
        ),
        label="имя пользователя",
    )
    password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(
            attrs={"class": "form-control mb-1", "placeholder": "Пароль"}
        ),
        label="Пароль",
    )
    remember_me = forms.BooleanField(required=False, label="Запомнить меня")
    recaptcha = ReCaptchaField()

    class Meta:
        """Метакласс формы, определяющий модель и поля, используемые в форме."""

        model = get_user_model()
        fields = ["username", "password", "remember_me"]


class UpdateUserForm(forms.ModelForm):
    """Форма для обновления данных пользователя."""

    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-1", "placeholder": "Имя пользователя"}
        ),
        label="Имя пользователя",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control mb-1", "placeholder": "Электронная почта"}
        ),
        label="Электронная почта",
    )

    class Meta:
        """Метакласс формы, определяющий модель и поля, используемые в форме."""

        model = get_user_model()
        fields = ["username", "email"]

    def clean_email(self):
        """Проверка уникальности email адреса."""

        email = self.cleaned_data.get("email")
        if (
            email
            and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        ):
            raise forms.ValidationError("Email адрес должен быть уникальным")
        return email


class UpdateProfileForm(forms.ModelForm):
    """Форма для обновления профиля пользователя."""

    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control mb-1"}),
        validators=IMAGE_VALIDATORS,
        label="Аватар",
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control"}),
        label="Биография",
    )

    class Meta:
        """Метакласс формы, определяющий модель и поля, используемые в форме."""

        model = Profile
        fields = ["avatar", "bio"]
