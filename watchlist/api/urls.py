from django.db import models
#from watchlist.api.views import movie_list, movie_detail       #for function based views
from watchlist.api.views import MovieListAV, MovieDetailsAV     #for class based views
from django.urls import path, include

urlpatterns = [
    #function based views
    # path('list/',movie_list, name='movie-list'),
    # path('<int:pk>',movie_detail, name='movie-detail'),
    
    #class based views
    path('list/', MovieListAV.as_view(), name= 'movie-list'),
    path('<int:pk>', MovieDetailsAV.as_view(), name = 'movie-details')
]