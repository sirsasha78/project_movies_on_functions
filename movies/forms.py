from django import forms


class EmailMovieForm(forms.Form):
    """Форма для отправки электронной почты."""

    name = forms.CharField(max_length=25, label="Имя")
    email = forms.EmailField(label="Электронная почта")
    to = forms.EmailField(label="Адрес получателя")
    comments = forms.CharField(
        required=False, widget=forms.Textarea, label="Комментарий"
    )
