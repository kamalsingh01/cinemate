from django.db import models
#from watchlist.api.views import movie_list, movie_detail       #for function based views
from watchlist.api.views import (WatchListAV, WatchListDetailsAV,
                                StreamPlatformAV, StreamPlatformDetailsAV, 
                                ReviewList, ReviewDetail, CreateReview, StreamPlatformViewSet)    #for class based views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'stream', StreamPlatformViewSet, basename='streamplatform')

urlpatterns = [
    #function based views
    # path('list/',movie_list, name='movie-list'),
    # path('<int:pk>',movie_detail, name='movie-detail'),
    
    #class based views
    path('list/', WatchListAV.as_view(), name= 'movie-list'),
    path('<int:pk>', WatchListDetailsAV.as_view(), name = 'watchlist-details'),

    path('',include(router.urls)),
    # path('stream/', StreamPlatformAV.as_view(),name = 'platform-list'),
    # path('stream/<str:slug>', StreamPlatformDetailsAV.as_view(), name = 'platform-details'),


    # path('review/', ReviewList.as_view(), name = 'review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name = 'review-detail')

    path('<int:pk>/review/', ReviewList.as_view(), name = 'review-details'),
    path('<int:pk>/review-create/', CreateReview.as_view(), name = 'create-review'),
    path('review/<int:pk>', ReviewDetail.as_view(), name = 'review-detail')


]