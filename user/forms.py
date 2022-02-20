from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput
                               (attrs={'placeholder': 'Username',
                                       'class': 'form-control'}), label="", )
    password = forms.CharField(max_length=128,
                               widget=forms.PasswordInput
                               (attrs={'placeholder': 'Password',
                                       'class': 'form-control', 'id': 'id_password'}), label="")


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
                               label="")
    first_name = forms.CharField(max_length=150,
                                 widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'First Name'}),
                                 label="")
    last_name = forms.CharField(max_length=150,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                                label="")
    email = forms.CharField(max_length=128,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label="")
    password = forms.CharField(max_length=128,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password',
                                                                 'id': 'id_password'}), label="")
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'id_cpassword', 'placeholder': 'Confirm Password'}), label="")

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('This username is taken')
        return self.cleaned_data['username']

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Password donot match')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image']
