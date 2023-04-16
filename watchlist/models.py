from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

'''
> One stream platform can have multiple movies but one movvie can only be present on one platform

'''

#streamplatform
class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    website = models.URLField(max_length=100)
    about = models.CharField(max_length=100)
    slug =models.SlugField(default = "", null = False) 

    def __str__(self) -> str:
        return self.name

#Watchlist
class WatchList(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length = 250)
    category = models.CharField(
        max_length=30,
        choices = [
        ('Movie','Movie'),
        ('WebSeries','WebSeries'),
        ('Podcast','Podcast'),
        ('Documentary','Documentary')
        ],
        default = 'Movie'
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    genre = models.CharField(
        max_length=30,
        choices = [
        ('Action','Action'),
        ('Thriller','Thriller'),
        ('Non-fiction','Non-fiction'),
        ('Comedy','Comedy'),
        ('RomCom','RomCom'),
        ('Drama','Drama'),
        ],
        default = 'Non-Fiction'
    )
    is_active = models.BooleanField(default=True)
    platform = models.ForeignKey(StreamPlatform, default = " ", on_delete=models.SET_DEFAULT, related_name="watchlist")
    #in Db, foriegn key is basically represented by an integer field which is primary key of forigen object.
    #related_name is used for reverse relationship

    #adding custom calculations, average rating and number of reviews, and they get updated after every review addition
    avg_rating = models.FloatField(default=0)
    number_of_rating = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title # + self.genre

class Reviews(models.Model): 
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=200, null=True)
    is_active  = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating) + " " + self.watchlist.title

class Movies(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True) #if movie published or not
    description =models.TextField(max_length=250) 

    def __str__(self) -> str:
        return self.title
    
    