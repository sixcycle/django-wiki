from SixcycleWiki.authentication.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect


class MyBackend:
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        user = User.objects.filter(
                email=username
        ).first()
        if (user and
                user.check_password(password) and
                self.user_can_authenticate(user)):
            return user

    def user_can_authenticate(self, request):
        return True

    def get_user(self, user_id):
        user = User.objects.filter(
            id=user_id
        ).first()
        return user


class TokenFromQueryParameterBackend:
    def authenticate(self, request, *args, **kwargs):
        # Check the username/password and return a user.
        user = None
        token = kwargs.get("token", None)
        if token:
            user = User.objects.get(auth_token=token)
            user.backend = 'allauth.account.auth_backends.AuthenticationBackend'
            login(request, user)
            request.user = user
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
