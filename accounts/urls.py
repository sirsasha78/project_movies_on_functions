from django.urls import path
from .views import SignUpView, CustomLoginView, profile, ChangePasswordView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "login/",
        CustomLoginView.as_view(
            redirect_authenticated_user=True, template_name="registration/login.html"
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    path("profile/", profile, name="profile"),
    path("password_change/", ChangePasswordView.as_view(), name="password_change"),
]
