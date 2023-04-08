# from django.shortcuts import render
# from .models import Movies
# from django.http import JsonResponse #helps sending response in the form of JSON, when we do not need to send HTTP response or render a template


# def movie_list(request):
#     queryset = Movies.objects.all();    #complex data type
#     #serialization without serializer
#     data = {
#         'movies' : list(queryset.values())
#     }
#     # JsonResponse() takes dictionary as parameter
#     return JsonResponse(data)  # JSON response(not dictionary) means - True becomes true and all doube quotes.

# def movie_detail(request,id):
#     queryset = Movies.objects.get(id = id)  #with get() method we only get object name(returning from __str__ function in Movie model)
#     # print(queryset)
#     # print(queryset.values())
#     # data = {
#     #     'movie-detail': list(queryset.values())
#     # }
#     #if we use get()
#     data = {
#         'name' : queryset.title,
#         'genre' : queryset.genre,
#         'is_active': queryset.is_active,
#         'description' : queryset.description
#     }
#     return JsonResponse(data)