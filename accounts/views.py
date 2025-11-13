from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, UpdateUserForm, UpdateProfileForm


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


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    """Отображает и обрабатывает форму профиля пользователя."""

    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Ваш профиль успешно обновлён.")
            return redirect("profile")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(
        request,
        "registration/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "registration/change_password.html"
    success_message = "Ваш Пароль был успешно изменен"
    success_url = reverse_lazy("profile")
