from rest_framework import serializers
from watchlist.models import Movies

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title= serializers.CharField(max_length=100)
    genre = serializers.CharField()
    is_active = serializers.BooleanField(default=True)
    description = serializers.CharField(max_length = 250) 

    #for POST
    def create(self, validated_data):
        return Movies.objects.create(**validated_data)  #validated_data has multiple argument passed from frontend application.
        #creating an object of ModelName class using data from frontend pushed using POST and passing it to corresponding view.

    def update(self, instance, validated_data):  #instance carries old values of the selected object and validated data carries new values
        #in update, we need to update old values with new values
        instance.title = validated_data.get('title',instance.title)
        instance.genre = validated_data.get('genre',instance.genre)
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance
