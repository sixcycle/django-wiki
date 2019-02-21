from SixcycleWiki.authentication.models import ProxyUser


class MyBackend:
    def authenticate(self, request, username=None, password=None):
        # Check the username/password and return a user.
        user = ProxyUser.objects.filter(
                email=username
        ).first()
        if (user and
                user.check_password(password) and
                self.user_can_authenticate(user)):
            return user

    def user_can_authenticate(self, request):
        return True

    def get_user(self, user_id):
        user = ProxyUser.objects.filter(
            id=user_id
        ).first()
        return user
