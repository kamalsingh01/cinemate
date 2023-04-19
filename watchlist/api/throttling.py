#Custom throttling ratesa and scopes
from rest_framework.throttling import UserRateThrottle


#restricting user to create only one review in a day
class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'
    #define the rate in settings.py

class ReviewListThrottle(UserRateThrottle):
    scope = 'review-list'
    #define the rate in settings.py