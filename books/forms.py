from django.forms import ModelForm, TextInput
from django import forms
from .models import Books


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['name', 'url', 'cast', 'description', 'category', 'movie_image']
        exclude = ['info_user']
        widgets = {
            'cast': forms.TextInput(attrs={'class': 'form_cast'}),
        }
