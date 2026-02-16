from django import forms
from django_recaptcha.fields import ReCaptchaField
from .models import Comment, Movie


class EmailMovieForm(forms.Form):
    """Форма для отправки электронной почты."""

    name = forms.CharField(
        max_length=25,
        label="Имя",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control mb-1", "placeholder": "Имя"}
        ),
    )
    email = forms.EmailField(
        label="Электронная почта",
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control mb-1", "placeholder": "Электронная почта"}
        ),
    )
    to = forms.EmailField(
        label="Адрес получателя",
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control mb-1", "placeholder": "Кому"}
        ),
    )
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control mb-1", "placeholder": "Комментарий"}
        ),
        label="Комментарий",
    )


class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев."""

    recaptcha = ReCaptchaField()

    class Meta:
        """Метакласс формы, определяющий модель и поля, используемые в форме."""

        model = Comment
        fields = ("name", "email", "body")
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Имя"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Электронная почта"}
            ),
            "body": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Текст"}
            ),
        }
        labels = {
            "name": "Имя пользователя",
            "email": "Электронная почта",
            "body": "Текст комментария",
        }


class AddMovieForm(forms.ModelForm):
    """Форма для добавления фильма."""

    class Meta:
        """Метакласс формы, определяющий модель и поля, используемые в форме."""

        model = Movie
        fields = (
            "title",
            "description",
            "trailer",
            "year",
            "rating",
            "genre",
            "director",
            "photo",
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "trailer": forms.URLInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "genre": forms.Select(attrs={"class": "form-control"}),
            "director": forms.Select(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
        }


class MovieUpdateForm(AddMovieForm):
    """Форма для обновления фильма."""

    class Meta(AddMovieForm.Meta):
        """Метакласс формы, определяющий модель и поля, используемые в форме."""

        pass
