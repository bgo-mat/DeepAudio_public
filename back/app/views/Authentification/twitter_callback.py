import os

from django.http import HttpResponseRedirect
from django.conf import settings
from allauth.socialaccount.providers.twitter.views import oauth_callback
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login

IN_PROD = os.getenv("IN_PROD", "True") == "True"


class TwitterAuthCallbackView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        # Délègue la gestion du callback à django-allauth
        response = oauth_callback(request)

        # Vérifie si l'utilisateur a été authentifié
        if request.user.is_authenticated:
            # Génère les tokens JWT pour l'utilisateur
            user = request.user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Prépare la réponse de redirection
            response = HttpResponseRedirect(settings.FRONTEND_URL)

            # Définit les cookies pour les tokens
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=IN_PROD,
                samesite="None",  # if IN_PROD else 'Lax',
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=IN_PROD,
                samesite="None",  # if IN_PROD else 'Lax',
            )

            return response
        else:
            # En cas d'échec de l'authentification, redirige avec une erreur
            return HttpResponseRedirect(
                f"{settings.FRONTEND_URL}?error=authentication_failed"
            )
