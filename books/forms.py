from django.forms import ModelForm, TextInput
from django import forms
from .models import Books


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['name', 'authors', 'description', 'category', 'book_image']
        exclude=['info_user']
