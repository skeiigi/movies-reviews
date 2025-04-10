from django import forms
from .models import Movies, Reviews


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['title', 'poster', 'about']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['title', 'movie', 'content']