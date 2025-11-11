from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignUpForm(UserCreationForm):
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
