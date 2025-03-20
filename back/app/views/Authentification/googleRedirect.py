from django.conf import settings
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.http import HttpResponseRedirect


def redirect_to_google_login(request):
    params = {
        "client_id": settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": request.build_absolute_uri("/api/auth/google/callback/"),
        "response_type": "code",
        "scope": "openid email profile",
    }
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
    response = HttpResponseRedirect(google_auth_url)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return response
