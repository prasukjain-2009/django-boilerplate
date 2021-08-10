from re import sub
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from rest_framework.request import Request
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


def get_user_jwt(request):
    """
    Replacement for django session auth get_user & auth.get_user for
     JSON Web Token authentication. Inspects the token for the user_id,
     attempts to get that user from the DB & assigns the user on the
     request object. Otherwise it defaults to AnonymousUser.
    This will work with existing decorators like LoginRequired, whereas
    the standard restframework_jwt auth only works at the view level
    forcing all authenticated users to appear as AnonymousUser ;)
    Returns: instance of user object or AnonymousUser object
    """
    user = None
    try:
        user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
    except:
        pass

    return user or AnonymousUser()

class JWTAuthenticationMiddleware(MiddlewareMixin):

    def process_request(self, request):
        token = request.META.get("HTTP_AUTHORIZATION",None)
        if token:
            request.user = SimpleLazyObject(lambda : get_user_jwt(request))
        else:
            pass
    
