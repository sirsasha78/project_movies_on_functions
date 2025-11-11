from urllib import request
from django.http import HttpRequest, HttpResponse
from .forms import SignUpForm, LoginForm
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView


class SignUpView(generic.CreateView):
    """Представление для регистрации нового пользователя."""

    form_class = SignUpForm
    template_name = "registration/signup.html"

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Перехватывает HTTP-запрос и проверяет, аутентифицирован ли пользователь.
        Если пользователь уже вошёл в систему, он перенаправляется на страницу
        со списком фильмов. В противном случае запрос передаётся дальше для обработки.
        """

        if request.user.is_authenticated:
            return redirect("movies:movie_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: SignUpForm) -> HttpResponse:
        """Обрабатывает валидную форму регистрации."""

        form.save()
        username = form.cleaned_data.get("username")
        messages.success(self.request, f"Учётная запись создана для {username}")
        return redirect("login")


class CustomLoginView(LoginView):
    """Представление для входа в систему с использованием формы."""

    form_class = LoginForm

    def form_valid(self, form: LoginForm) -> HttpResponse:
        """Перехватывает валидную форму и устанавливает сессию пользователя."""

        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)
