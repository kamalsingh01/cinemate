from watchlist.models import Movies
from rest_framework.response import Response
from rest_framework import status  #for status codes
from .serializers import MovieSerializer
from rest_framework.decorators import api_view
from django.shortcuts import render
from django.http import HttpResponse

@api_view(['GET','POST'])   #y default it takes GET.
def movie_list(request):
    #handling GET request
    if request.method == 'GET':
        movie = Movies.objects.all()
        serializer = MovieSerializer(movie, many=True)  
        #NOTE:# many=True is important when dealing with multiple objects, it lets serializer to reach multiple object attriutes/elements and map it with serializer fields.
        #print(serializer)
        #print(serializer.data)
        return Response(serializer.data)
    #handling POST request(no return)
    elif request.method == 'POST':
        # serialization -> Validation -> Create the complex object
        serializer = MovieSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET','PUT','DELETE'])
def movie_detail(request,pk):
    if request.method == 'GET':

        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
             return Response({'Error':'Match not Found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        movie = Movies.objects.get(pk=pk) 
        serializer = MovieSerializer(movie, data = request.data) #passing movie cuz defining which object to be updated
        if serializer.is_valid():
            serializer.update()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    elif request.method == 'DELETE':
        movie = Movies.objects.get(pk=pk)
        #serializer = MovieSerializer(movie)
        movie.delete()
        #return Response(serializer.data)
        #data = {'msg':'record Delete'}
        return Response(status=status.HTTP_204_NO_CONTENT)

'''
In Function based views (with Serializer class) we need to add decorators to eah view
which takes the list of HTTP methods that the view should respond to.

GET() - reading the data
POST - writing or storing data to the database
PUT - updating data in sb
DELETE - deleting some oject in db.

> Because we are using rest_framwork.response we get API responses in a detailed manner as  abrowsable API.

> When we work with POST and PUT , we use create() and update methods under serializer class

> STATUS CODES : action codes on the Web that signifies any action performed on web




'''