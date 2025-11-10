from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label="Имя пользователя")
    email = forms.EmailField(max_length=200, label="Электронная почта")

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]
