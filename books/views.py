from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from user.models import Category
from .forms import BookForm
from .models import Books, History
from notifications.models import Notification
from book_recommendation.settings import MEDIA_URL
import nltk
import re
import numpy as np
import contractions
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

nltk.download('punkt')


# Create your views here.
def MyItems(request):
    if request.method == 'POST':
        print(request.POST)
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            print('form is valid')
            add_user = form.save(commit=False)
            add_user.info_user = request.user
            add_user.save()
            Notification.objects.create(message=f'{request.user} have added a new book {request.POST["name"]}',
                                        user=request.user)
            return redirect("recently_added")

    elif request.method == 'GET':
        form = BookForm()
    context = {
        'form': form,
        'menuindex': 4

    }
    return render(request, 'books/my_items.html', context)


class BookDetailView(DetailView):
    model = Books

    def get_context_data(self, **kwargs):
        History.objects.create(user=self.request.user, book=Books.objects.get(id=self.kwargs['pk']))
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['MEDIA_URL'] = MEDIA_URL
        return context


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Books
    fields = ['name', 'authors', 'description', 'category', 'book_image']
    success_url = '/'

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


def book_history(request):
    history = History.objects.filter(user_id=request.user.id).order_by("created_at")[::-1][:5]
    book_name_list = []
    for h in history:
        book_name = h.book.name
        book_name_list.append(book_name)
    book_name_set = set(book_name_list)  # to retrieve only the unique book name
    return book_name_set


def normalize_document(doc):
    # lower case and remove special characters\whitespaces
    doc = re.sub(r'[^a-zA-Z0-9\s]', '', doc, re.I | re.A)
    doc = doc.lower()
    doc = doc.strip()
    doc = contractions.fix(doc)
    # tokenize document
    tokens = nltk.word_tokenize(doc)
    stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
                  "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",
                  'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs',
                  'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is',
                  'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
                  'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at',
                  'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',
                  'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                  'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
                  'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
                  'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've",
                  'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn',
                  "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
                  'ma', 'mightn', "mightn't", 'must', 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
                  'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

    # filter stopwords out of document
    filtered_tokens = [token for token in tokens if token not in stop_words]
    # re-create document from filtered tokens
    doc = ' '.join(filtered_tokens)
    return doc


tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=2)

# creating dataframe for recommendation engine
books_object = list(Books.objects.values())
books_df = pd.DataFrame(books_object)

category_object = list(Category.objects.values())
category_df = pd.DataFrame(category_object)

category_df.columns = ['category_id', 'category_name']
main_data = books_df.merge(category_df, how="left", on="category_id")

# preprocessing
normalized_corpus = np.vectorize(normalize_document)
norm_corpus = normalized_corpus(list(main_data['description']))

df = pd.DataFrame({'description': norm_corpus,
                   'category': np.array(main_data['category_name'])})

# vectorization
tfidf_matrix = tfidf.fit_transform(df['description'] + df['category'])
print(tfidf_matrix.shape)

# similarity_scores
doc_sim = cosine_similarity(tfidf_matrix)
doc_sim_df = pd.DataFrame(doc_sim)

# finding given book id
book_list = main_data['name'].values


def recommender_engine(book_title):
    book_idx = np.where(book_list == str(book_title))[0][0]
    book_similarities = doc_sim_df.iloc[book_idx].values
    similar_book_idxs = np.argsort(-book_similarities)[1:3]
    similar_book = book_list[similar_book_idxs]

    return similar_book


def RecentlyAdded(request):
    u = User.objects.all()
    desc = Books.objects.all()
    return render(request, 'books/recently_added.html',
                  {'desc': desc, 'u': u, 'MEDIA_URL': MEDIA_URL, "menuindex": 3, "heading": "Recently Added Books"})


def recommend_books(request):
    book_name_set = book_history(request)
    similar_books = []
    for i in book_name_set:
        similar_book = recommender_engine(i)
        similar_books.append(similar_book)

    bookList = [item for elem in similar_books for item in elem]
    sb = set(bookList)
    print("SB:", sb)
    l = []
    for i in sb:
        l.append(Books.objects.filter(name=i).last())
    print("L:", l)
    return render(request, 'books/recommended_books.html',
                  {'MEDIA_URL': MEDIA_URL, "menuindex": 6, "desc": l, "heading": "Recommended Books"})
