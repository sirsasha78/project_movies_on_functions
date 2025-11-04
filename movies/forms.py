from django import forms
from .models import Comment


class EmailMovieForm(forms.Form):
    """Форма для отправки электронной почты."""

    name = forms.CharField(max_length=25, label="Имя")
    email = forms.EmailField(label="Электронная почта")
    to = forms.EmailField(label="Адрес получателя")
    comments = forms.CharField(
        required=False, widget=forms.Textarea, label="Комментарий"
    )


class CommentForm(forms.ModelForm):
    """Форма для добавления комментариев."""

    class Meta:
        """Метакласс формы, определяющий модель и поля, используемые в форме."""

        model = Comment
        fields = ("name", "email", "body")
