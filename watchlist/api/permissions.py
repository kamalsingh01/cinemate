from rest_framework import permissions
from django.contrib.auth.models import User

#creating permission : admin can do all bbut other can read only.

class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view): #wreturns boolen values
        admin_permission = bool(request.user and request.user.is_staff) 
        print(request.user)
        print(request.user.is_staff)
        #above we check if requested user is a user and is also an admin(is_staff) 
        return request.method == "GET" or admin_permission
    
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

class ReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
        #check permission for read-only request
            return True         #permiting to go ahead
        else:
        #check permission for write request
            return (obj.review_user == request.user)
            # other users won't get to perform write operations other than review user
