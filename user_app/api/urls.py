from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import registration_view, logout_view

urlpatterns = [
    path('login/', obtain_auth_token, name = 'login'),      # obtain_auth_token view class generates a token and maps it with the username and pass
    path('register/',registration_view, name='register'),
    path('logout/',logout_view, name = 'logout'),
    
]