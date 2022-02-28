from django.urls import path
from .views import MyItems, RecentlyAdded, BookDetailView, BookUpdateView, BookDeleteView, search, recommend_books
urlpatterns = [
    path("myitems/", MyItems, name="my_books"),
    path("recently_added", RecentlyAdded, name="recently_added"),
    path('detail/<int:pk>/',BookDetailView.as_view(),name='detail'),
    path('detail/<int:pk>/update/', BookUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/delete/', BookDeleteView.as_view(), name='delete'),
    path('search/', search, name='search'),
    path('recommend', recommend_books, name="recommend")
]
