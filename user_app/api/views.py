from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app.models import *   #importing this will help generating token for the specigic user.
from rest_framework import status

# Create your views here.

#logout
@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST' :
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

#registration
@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data = request.data)

        #empty dictionary which stores all the data to be sent back as response, including username, email and token
        data = {}

        if serializer.is_valid():
            account = serializer.save()   # overriden save() method runs and return account variable\
            #we get the data, now we will fill the dictionary object
            data['response'] = 'Registration Successful'
            data['username'] = account.username
            data['email'] = account.email
            #now fetching generated token from token class for the user instance generated from overriden save() method
            token = Token.objects.get(user = account).key  
            data['token'] = token

            #for existing users we can create as :
            # for user in User.objects.all():
            #     Token.objects.get_or_create(user=user)
        else:
            data = serializer.errors

            
        return Response(data)
