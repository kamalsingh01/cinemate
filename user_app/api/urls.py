from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from .views import registration_view, logout_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [

    #for tokenAuthentication
    # # obtain_auth_token view class generates a token and maps it with the username and pass
    path('login/', obtain_auth_token, name = 'login'),      
    path('register/',registration_view, name='register'),
    path('logout/',logout_view, name = 'logout'),

    #for JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]