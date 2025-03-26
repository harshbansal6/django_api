from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class CookieAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.COOKIES.get('auth_token')
        if not auth_token:
            return None

        try:
            user = User.objects.get(auth_token=auth_token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None) 