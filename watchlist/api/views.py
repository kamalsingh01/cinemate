from watchlist.models import WatchList, StreamPlatform, Reviews
from rest_framework.response import Response
from rest_framework import status  #for status codes
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework.decorators import api_view  #for function based views
from rest_framework.views import APIView        #for class based views
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from watchlist.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly

# from rest_framework import mixins
from rest_framework import generics

# CLASS_BASED_VIEWS: 
                                    #ITS NOT OVER UNTIL ITS OVER

# GENERIC API VIEW : Concrete Classes.

class ReviewList(generics.ListAPIView):     # ListApiView gives get() and post() methods
    # queryset = Reviews.objects.all()
    serializer_class  = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    #method to overwrite queryset based on requirement
    def get_queryset(self):
        pk = self.kwargs['pk']  #accessing primary key  - self id reviews class object
        return Reviews.objects.filter(watchlist=pk) #getting movie objects where movie id is pk,
        #filter() pulls out multiple objects while get() only pulls one



class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly ]  

class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
 
    def get_queryset(self):
        return Reviews.objects.all()

    def perform_create(self, serializer):       # generic class class this to POST
        pk = self.kwargs['pk']
        movie = WatchList.objects.get(pk=pk)

        # checking if any review already exists for the user
        review_user = self.request.user
        review_queryset = Reviews.objects.filter(watchlist = movie, review_user = review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviwed this screenplay.")

        # if no review present fot the current screenplay
        if movie.number_of_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating +  serializer.validated_data['rating'])/2
        
        movie.number_of_rating +=1
        movie.save()
        
        serializer.save(watchlist = movie, review_user = review_user)

    # def per(self):
    #     pk = self.kwargs['pk']
    #     return Reviews.objects.create(watchlist = pk)


# generic API Views using mixins
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Reviews.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

#     queryset = Reviews.objects.all()        # queryset and serializer_classes are actually defualt names.
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

class StreamPlatformViewSet(viewsets.ViewSet):

    def list(self,request): 
        queryset = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(queryset, many=True )
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = StreamPlatform.objects.all()
        watchlist = get_object_or_404(queryset, pk=pk)
        serializer = StreamPlatformSerializer(watchlist)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = StreamPlatformSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def destroy(self, request,pk):
        platform = StreamPlatform.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
'''Using ModelViewset

class StreamPlatformViewSet(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

there are other viewset like ReadOnlyModelViewset, etc.
'''


class StreamPlatformAV(APIView):

    def get(self,request):
        platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(platforms, many=True) #context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer( data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class StreamPlatformDetailsAV(APIView):
    
    def get(self, request, slug):
        try:
            platform = StreamPlatform.objects.get(slug = slug) 
        except StreamPlatform.DoesNotExist:
             return Response({'msg':'Streaming Platform Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)
    
    def put(self, request, slug):
        platform = StreamPlatform.objects.get(slug = slug)
        serializer = StreamPlatformSerializer(platform, data = request.data)
        if serializer.is_valid():  
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, requst,slug):
        platform = StreamPlatform.objects.get(slug=slug)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        

class WatchListAV(APIView):

    #methods
    def get( self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many = True)
        return Response(serializer.data)
 
    def post( self, request):
        serializer = WatchListSerializer(data = request.data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    

class WatchListDetailsAV(APIView):


    #methods
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotexist:
            return Response({'msg':'Movie Not Found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WatchListSerializer(movie)
        return Response(serializer.data)
    
    def put(self,request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)










'''FUNCTION_BASED_VIEWS:''' 

# @api_view(['GET','POST'])   #y default it takes GET.
# def movie_list(request):
#     #handling GET request
#     if request.method == 'GET':
#         movie = Movies.objects.all()
#         serializer = MovieSerializer(movie, many=True)  
#         #NOTE:# many=True is important when dealing with multiple objects, it lets serializer to reach multiple object attriutes/elements and map it with serializer fields.
#         #print(serializer)
#         #print(serializer.data)
#         return Response(serializer.data)
#     #handling POST request(no return)
#     elif request.method == 'POST':
#         # serialization -> Validation -> Create the complex object
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid(): 
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET','PUT','DELETE'])
# def movie_detail(request,pk):
#     if request.method == 'GET':

#         try:
#             movie = Movies.objects.get(pk=pk)
#         except Movies.DoesNotExist:
#              return Response({'Error':'Match not Found'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         movie = Movies.objects.get(pk=pk)  #getting instance data(MovieSerializer)
#         serializer = MovieSerializer(movie, data = request.data) #passing movie cuz defining which object to be updated 
#         if serializer.is_valid():    #is_valid runs and control moves to update function in Movie Serializer.
#             serializer.update()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
#     elif request.method == 'DELETE':
#         movie = Movies.objects.get(pk=pk)
#         #serializer = MovieSerializer(movie)
#         movie.delete()
#         #return Response(serializer.data)
#         #data = {'msg':'record Delete'}
#         return Response(status=status.HTTP_204_NO_CONTENT)

# '''
# In Function based views (with Serializer class) we need to add decorators to eah view
# which takes the list of HTTP methods that the view should respond to.

# GET() - reading the data
# POST - writing or storing data to the database
# PUT - updating data in sb
# DELETE - deleting some oject in db.

# > Because we are using rest_framwork.response we get API responses in a detailed manner as  abrowsable API.

# > When we work with POST and PUT , we use create() and update methods under serializer class

# > STATUS CODES : action codes on the Web that signifies any action performed on web




# '''