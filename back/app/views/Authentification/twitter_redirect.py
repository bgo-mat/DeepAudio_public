from django.shortcuts import redirect
from allauth.socialaccount.providers.twitter.views import oauth_login


def redirect_to_twitter_login(request):
    return oauth_login(request)
