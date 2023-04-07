from django.db import models
from watchlist.views import movie_list, movie_detail
from django.urls import path, include

urlpatterns = [
    path('',movie_list, name='movie-list'),
    path('<int:id>',movie_detail, name='movie-detail'),
]