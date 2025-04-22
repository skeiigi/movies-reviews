from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Movies, Reviews


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", max_length=150)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name in self.fields:
            self.fields[field_name].help_text = None

        self.fields["username"].widget.attrs.update(
            {"id": "id_username", "placeholder": " "}
        )
        self.fields["email"].widget.attrs.update(
            {"id": "id_email", "placeholder": " "}
        )  # noqa: E501
        self.fields["password1"].widget.attrs.update(
            {"id": "id_password1", "placeholder": " "}
        )
        self.fields["password2"].widget.attrs.update(
            {"id": "id_password2", "placeholder": " "}
        )


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['title', 'poster', 'about']

        labels = {
            "title": "Название",
            "poster": "Фото",
            "about": "Описание"
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['title', 'movie', 'content']

        labels = {
            "title": "Название",
            "movie": "Фильм",
            "content": "Текст"
        }