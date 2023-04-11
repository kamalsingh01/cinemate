from django.contrib import admin
from .models import Movies,WatchList, StreamPlatform, Reviews

# Register your models here.

admin.site.register(Movies)
admin.site.register(WatchList)
admin.site.register(StreamPlatform)
admin.site.register(Reviews)
