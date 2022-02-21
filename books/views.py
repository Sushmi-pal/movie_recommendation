from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import BookForm
from .models import Books
from book_recommendation.settings import MEDIA_URL


# Create your views here.
def MyItems(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            print('form is valid')
            add_user = form.save(commit=False)
            add_user.info_user = request.user
            add_user.save()

    elif request.method == 'GET':
        form = BookForm()
    context = {
        'form': form,
        'menuindex':4

    }
    return render(request, 'books/my_items.html', context)


def RecentlyAdded(request):
    u = User.objects.all()
    desc = Books.objects.all()
    return render(request, 'books/recently_added.html', {'desc': desc, 'u': u, 'MEDIA_URL': MEDIA_URL, "menuindex": 3})


class BookDetailView(DetailView):
    model = Books

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['MEDIA_URL'] = MEDIA_URL
        return context


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Books
    fields = ['name', 'authors', 'description', 'category', 'book_image']

    def form_valid(self, form):
        form.instance.info_user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        desc = self.get_object()
        if self.request.user == desc.info_user:
            return True
        return False


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Books
    success_url = '/'

    def test_func(self):
        desc = self.get_object()
        if self.request.user == desc.info_user:
            return True
        return False

def search(request):
    query = request.GET['query']
    if len(query) > 85:
        book = []
    else:
        Bname = Books.objects.filter(name__icontains=query)
        Bdesc = Books.objects.filter(description__icontains=query)
        book = Bname.union(Bdesc)
    params = {'book': book, 'query': query}
    return render(request, 'books/search.html', params)
