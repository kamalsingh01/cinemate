from django.db import models
from watchlist.api.views import movie_list, movie_detail
from django.urls import path, include

urlpatterns = [
    path('list/',movie_list, name='movie-list'),
    path('<int:pk>',movie_detail, name='movie-detail'),

]