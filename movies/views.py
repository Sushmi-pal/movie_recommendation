from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from user.models import Category
from .forms import MovieForm
from .models import Movies, History
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
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            print('form is valid')
            add_user = form.save(commit=False)
            add_user.info_user = request.user
            add_user.save()
            Notification.objects.create(message=f'{request.user} have added a new movie {request.POST["name"]}',
                                        user=request.user)
            return redirect("recently_added")

    elif request.method == 'GET':
        form = MovieForm()
    context = {
        'form': form,
        'menuindex': 4

    }
    return render(request, 'movies/my_items.html', context)


class MovieDetailView(DetailView):
    model = Movies
    template_name = "movies/movies_detail.html"

    def get_context_data(self, **kwargs):
        History.objects.create(user=self.request.user, movie=Movies.objects.get(id=self.kwargs['pk']))
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        context['MEDIA_URL'] = MEDIA_URL
        return context


class MovieUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Movies
    fields = ['name', 'cast', 'description', 'category', 'movie_image']
    success_url = '/'
    template_name = "movies/movies_form.html"

    def form_valid(self, form):
        form.instance.info_user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        desc = self.get_object()
        if self.request.user == desc.info_user:
            return True
        return False


class MovieDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Movies
    success_url = '/'
    template_name = "movies/movies_confirm_delete.html"

    def test_func(self):
        desc = self.get_object()
        if self.request.user == desc.info_user:
            return True
        return False


def search(request):
    query = request.GET['query']
    if len(query) > 85:
        movie = []
    else:
        Mname = Movies.objects.filter(name__icontains=query)
        Mdesc = Movies.objects.filter(description__icontains=query)
        movie = Mname.union(Mdesc)
        paginator = Paginator(list(movie), 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    params = {'page_obj': page_obj, 'query': query}
    return render(request, 'movies/search.html', params)


def movie_history(request):
    history = History.objects.filter(user_id=request.user.id).order_by("created_at")[::-1][:5]
    print("history", history)
    movie_name_list = []
    for h in history:
        movie_name = h.movie.name
        movie_name_list.append(movie_name)
    movie_name_set = set(movie_name_list)  # to retrieve only the unique movie name
    return movie_name_set


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


def get_movie_list():
    tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=2)

    # creating dataframe for recommendation engine
    movies_object = list(Movies.objects.values())
    movies_df = pd.DataFrame(movies_object)

    category_object = list(Category.objects.values())
    category_df = pd.DataFrame(category_object)

    category_df.columns = ['category_id', 'category_name']
    main_data = movies_df.merge(category_df, how="left", on="category_id")

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

    # finding given movie id
    movie_list = main_data['name'].values

    return doc_sim_df, movie_list


def recommender_engine(movie_title, movie_list, doc_sim_df):
    movie_idx = np.where(movie_list == str(movie_title))[0][0]
    movie_similarities = doc_sim_df.iloc[movie_idx].values
    similar_movie_idxs = np.argsort(-movie_similarities)[1:3]
    similar_movie = movie_list[similar_movie_idxs]

    return similar_movie


def RecentlyAdded(request):
    u = User.objects.all()
    desc = Movies.objects.all()
    paginator = Paginator(desc, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'movies/recently_added.html',
                  {'desc': desc, 'u': u, 'MEDIA_URL': MEDIA_URL, "menuindex": 3, "heading": "Recently Added Movies",
                   "page_obj": page_obj})


def get_recommended_movies(movie_name_set):
    doc_sim_df, movie_list = get_movie_list()
    similar_movies = []
    for i in movie_name_set:
        similar_movie = recommender_engine(i, movie_list=movie_list, doc_sim_df=doc_sim_df)
        similar_movies.append(similar_movie)
    movieList = [item for elem in similar_movies for item in elem]
    sb = set(movieList)
    return sb


def recommend_movies(request):
    movie_name_set = movie_history(request)
    try:
        sb = get_recommended_movies(movie_name_set)
    except:
        print("Error")
        sb = []

    l = []
    for i in sb:
        l.append(Movies.objects.filter(name=i).last())
    print("L:", l)
    paginator = Paginator(l, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("ppppppppppppppppppp", page_obj)
    return render(request, 'movies/recommended_movies.html',
                  {'MEDIA_URL': MEDIA_URL, "menuindex": 6, "page_obj": page_obj, "heading": "Recommended Movies"})
