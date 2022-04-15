from django.forms import ModelForm, TextInput
from django import forms
from .models import Movies


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movies
        fields = ['name', 'url', 'cast', 'description', 'category', 'movie_image']
        exclude = ['info_user']
        widgets = {
            'cast': forms.TextInput(attrs={'class': 'form_cast', 'rows': 4, 'cols': 4}),
            'description': forms.TextInput(attrs={'class': 'form_description', 'rows': 4, 'cols': 4}),

        }
