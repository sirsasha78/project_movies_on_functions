from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect, render


class AuthorRequiredMixin(AccessMixin):

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if not (self.user == self.get_object().author or request.user.is_staff):
                messages.info(
                    request, "Изменение нформации о фильме доступно только автору!"
                )
                return redirect("movies:movie_list")
        return super().dispatch(request, *args, **kwargs)
