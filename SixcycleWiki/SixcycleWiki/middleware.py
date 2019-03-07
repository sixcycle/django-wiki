from .authentication.models import User
from django.contrib.auth import login, authenticate


def LoginFromCookieMiddleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        token = request.GET.get("token", None)
        authenticate(request, token=token)
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
