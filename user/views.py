from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse

from books.models import Books
from .forms import LoginForm, SignupForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from book_recommendation.settings import MEDIA_URL
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Category, Profile
from notifications.models import Notification


# Create your views here.

def get_started(request):
    return redirect("signin")


def home(request):
    u = User.objects.all()
    desc = Books.objects.all()
    notifications=Notification.objects.all()
    return render(request, "books/home.html", {'desc': desc, 'u': u, 'MEDIA_URL': MEDIA_URL, "menuindex": 1})


def LoginView(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/user/profile')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user:
                print('user', user)
                login(request, user)
                return redirect('/user/profile/')
            else:
                print('Not authenticated')
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/user/profile/')
        form = LoginForm()
    return render(request, 'user/signin_form.html', {'form_login': form, "menuindex": 2})


def SignupView(request):
    if request.method == 'POST':
        print(request.POST)
        books = request.POST.getlist('books')
        print(books)

        form = SignupForm(request.POST)
        if form.is_valid() and len(books) > 0:
            print('form is valid')
            user = User(username=form.cleaned_data['username'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email'])
            user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            for i in books:
                b1 = Category.objects.get_or_create(
                    name=i)  # Results in (<Category: Category object (2)>, True). So, b1[0] to get the queryset
                b1[0].categories.add(user)
            print('user', user)
            Profile.objects.create(user=user)
            return redirect('signin')
        else:
            messages.error(request, "Please select the books type you like.")
    elif request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('profile')
        else:
            form = SignupForm()
    cat = Category.objects.all()

    return render(request, 'user/register_form.html', {'form_signup': form, 'categories': cat, "menuindex": 2})


def LogoutView(request):
    logout(request)
    return redirect('signin')


@login_required
@transaction.atomic
def ProfileView(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request,
                f'Your profile has been updated successfully'
            )
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'user_category': request.user.category_set.all(),
        'categories': Category.objects.all(),
        'menuindex': 5,
        'p_form': p_form
    }
    return render(request, 'user/profile.html', context)
