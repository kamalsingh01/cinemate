from django.db import models

# Create your models here.
class Movies(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True) #if movie published or not
    description =models.TextField(max_length=250) 

    def __str__(self) -> str:
        return self.title
    
    