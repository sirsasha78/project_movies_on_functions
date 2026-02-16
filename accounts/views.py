from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, UpdateUserForm, UpdateProfileForm
from .models import Profile
from typing import Any


class SignUpView(SuccessMessageMixin, generic.CreateView):
    """Представление для регистрации нового пользователя."""

    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = "Вы успешно зарегистрировались. Можете войти на сайт!"

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Перехватывает HTTP-запрос и проверяет, аутентифицирован ли пользователь.
        Если пользователь уже вошёл в систему, он перенаправляется на страницу
        со списком фильмов. В противном случае запрос передаётся дальше для обработки.
        """

        if request.user.is_authenticated:
            return redirect("movies:movie_list")
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(SuccessMessageMixin, LoginView):
    """Представление для входа в систему с использованием формы."""

    form_class = LoginForm
    success_message = "Добро пожаловать на сайт!"

    def form_valid(self, form: LoginForm) -> HttpResponse:
        """Перехватывает валидную форму и устанавливает сессию пользователя."""

        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


class ProfileView(UpdateView):
    """Представление для просмотра и редактирования профиля пользователя.
    Позволяет пользователю редактировать данные своего профиля и связанные
    с ним данные пользователя через веб-формы. Использует две формы:
    UpdateProfileForm — для данных профиля и UpdateUserForm — для данных пользователя.
    """

    model = Profile
    form_class = UpdateProfileForm
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        """Возвращает объект профиля, связанный с текущим пользователем.
        Переопределяет стандартное поведение, так как профиль не передаётся по ID в URL.
        """
        return self.request.user.profile

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Добавляет дополнительные данные в контекст шаблона."""

        context = super().get_context_data(**kwargs)
        context["title"] = f"Страница профиля: {self.request.user.username}"
        if self.request.POST:
            context["user_form"] = UpdateUserForm(
                self.request.POST, self.request.FILES, instance=self.request.user
            )
        else:
            context["user_form"] = UpdateUserForm(instance=self.request.user)
        return context

    def form_valid(self, form: UpdateProfileForm) -> HttpResponse:
        """Обрабатывает валидные данные обеих форм (профиля и пользователя)."""

        context = self.get_context_data()
        user_form = context["user_form"]
        if user_form.is_valid() and form.is_valid():
            user_form.save()
            form.save()
            messages.success(self.request, "Ваш профиль успешно обновлён.")
        return super().form_valid(form)

    def get_success_url(self):
        """Возвращает URL для перенаправления после успешного обновления профиля."""

        return reverse_lazy("profile")


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "registration/change_password.html"
    success_message = "Ваш Пароль был успешно изменен"
    success_url = reverse_lazy("profile")
