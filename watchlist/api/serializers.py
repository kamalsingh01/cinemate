from rest_framework import serializers
from watchlist.models import WatchList, StreamPlatform, Reviews

''' USING MODEL SERIALIZER CLASS '''

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Reviews
        #fields = "__all__"
        exclude = ['watchlist']

class WatchListSerializer(serializers.ModelSerializer):
    #custom serializer field - not present in our model but we can derive and display to client
    #title_len = serializers.SerializerMethodField()

    reviews = ReviewSerializer(many=True, read_only = True)


    class Meta:
        model = WatchList
        fields = "__all__"          # to include all the fields
        #fields = [ "id", "title", "description"]    - to incldue specific fields
        # exclude = ["is_active"]         - to exculde fields that we don't want, 
        #exclude , include and fields cannot be defined simultaneously


class StreamPlatformSerializer(serializers.ModelSerializer):
    #platfrom can have many movies

    watchlist = WatchListSerializer(many=True, read_only = True)  #related_name defined in model is used.
    #watchlist = serializers.StringRelatedField(many=True)   # fetches all fields from  model defined in __str__ method in the model
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='watchlist-details'
    # )
    class Meta:
        model = StreamPlatform
        fields = "__all__"

    


    
    #methods for custom serializer field
    # def get_title_len(self,object):  #object has access to all the data of our model object
    #     return len(object.title)

    #defining validations

    #field level validation
    # def validate_title(self, value):  #value contains the value of the validator field(e.g. title )
        
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too Short!")
    #     return value
        
    # #Object level Validation
    # def validate(self, data):
    #     if data['title'] == data['description']:
    #         raise serializers.ValidationError("Title and Description should be different")
    #     else:   #optional
    #         return data





''' USING SERIALIZER CLASS '''

# Using validator()
# def genre_length(value):    #method not inside class , so no need to add self.
#     if len(value) <=5:
#         raise serializers.ValidationError("not a valid Genre!!")


# class WatchListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title= serializers.CharField(max_length=100)
#     genre = serializers.CharField(validators = [ genre_length ])
#     is_active = serializers.BooleanField(default=True)
#     description = serializers.CharField(max_length = 250) 

#     #for POST
#     def create(self, validated_data):
#         return Watchlist.objects.create(**vwatchlist/reviews/alidated_data)  #validated_data has multiple argument passed from frontend application.
#         #creating an object of ModelName class using data from frontend pushed using POST and passing it to corresponding view.

#     #for PUT
#     def update(self, instance, validated_data):  #instance carries old values of the selected object and validated data carries new values
#         #in update, we need to update old values with new values
#         instance.title = validated_data.get('title',instance.title)
#         instance.genre = validated_data.get('genre',instance.genre)
#         instance.is_active = validated_data.get('is_active',instance.is_active)
#         instance.description = validated_data.get('description',instance.description)
#         instance.save()
#         return instance

#     #field level validation
#     # def validate_title(self, value):  #value contains the value of the validator field(e.g. title )
        
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too Short!")
#     #     return value
        
#     #Object level Validation
#     def validate(self, data):
#         if data['title'] == data['description']:
#             raise serializers.ValidationError("Title and Description should be different")
#         else:   #optional
#             return data
        