from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django_recaptcha.fields import ReCaptchaField

from .models import Movies, Reviews, Comment, MovieComment


class LoginForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(attrs={
            'data-theme': 'light',  # Опционально: светлая/темная тема
        }),
        error_messages={
            'required': 'Пожалуйста, подтвердите, что вы не робот'
        }
    )
    username = forms.CharField(label="Имя пользователя", max_length=150)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(attrs={
            'data-theme': 'light',  # Опционально: светлая/темная тема
        }),
        error_messages={
            'required': 'Пожалуйста, подтвердите, что вы не робот'
        }
    )

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
        )
        self.fields["password1"].widget.attrs.update(
            {"id": "id_password1", "placeholder": " "}
        )
        self.fields["password2"].widget.attrs.update(
            {"id": "id_password2", "placeholder": " "}
        )


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['id', 'title', 'poster', 'about', 'duration_minutes', 'country_release', 'year_of_release']

        labels = {
            "title": "Название",
            "poster": "Фото",
            "about": "Описание",
            "duration_minutes": "Продолжительность (мин)",
            "country_release": "Страна производства",
            "year_of_release": "Год производства"
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['id', 'title', 'movie', 'content']

        labels = {
            "title": "Название",
            "movie": "Фильм",
            "content": "Текст"
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Напишите комментарий...'})
        }

class MovieCommentForm(forms.ModelForm):
    class Meta:
        model = MovieComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Оставьте комментарий к фильму...'})
        }