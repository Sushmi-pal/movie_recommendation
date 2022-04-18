from django.urls import path
from .views import MyItems, RecentlyAdded, search, MovieDeleteView, MovieDetailView, MovieUpdateView, recommend_movies
urlpatterns = [
    path("myitems/", MyItems, name="my_books"),
    path("recently_added", RecentlyAdded, name="recently_added"),
    path('detail/<int:pk>/',MovieDetailView.as_view(),name='detail'),
    path('detail/<int:pk>/update/', MovieUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/delete/', MovieDeleteView.as_view(), name='delete'),
    path('search/', search, name='search'),
    path('recommend/', recommend_movies, name="recommend")
]
