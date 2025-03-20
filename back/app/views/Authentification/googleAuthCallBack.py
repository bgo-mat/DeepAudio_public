import os

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

IN_PROD = settings.IN_PROD
User = get_user_model()


class GoogleAuthCallbackView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        error = request.GET.get("error")
        if error:
            # Redirection si le user annule
            return HttpResponseRedirect(f"{settings.FRONTEND_URL}?error={error}")
        code = request.GET.get("code")
        if not code:
            return Response({"detail": "Code manquant dans l'URL"}, status=400)

        # Échanger le code contre un token Google
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID,
            "client_secret": settings.SOCIAL_AUTH_GOOGLE_CLIENT_SECRET,
            "redirect_uri": request.build_absolute_uri("/api/auth/google/callback/"),
            "grant_type": "authorization_code",
        }

        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        # Logguer la réponse de Google pour vérifier si l'échange du code fonctionne

        # Vérifie si Google a renvoyé une erreur
        if "error" in token_json:
            return Response(
                {"detail": token_json.get("error_description", "Erreur inconnue")},
                status=400,
            )

        # Vérifie si l'access token est présent
        access_token = token_json.get("access_token")
        if not access_token:
            return Response(
                {"detail": "Erreur lors de la récupération du token Google."},
                status=400,
            )

        # Récupérer les informations de l'utilisateur avec l'access token de Google
        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        user_info_params = {"access_token": access_token}
        user_info_response = requests.get(user_info_url, params=user_info_params)
        user_info = user_info_response.json()

        # Vérifie si l'email est présent
        email = user_info.get("email")
        if not email:
            return Response(
                {"detail": "Impossible de récupérer les informations utilisateur."},
                status=400,
            )

        # Vérifier si l'utilisateur existe déjà ou le créer
        user = User.objects.filter(email=email).first()
        if not user:
            try:
                user = User.objects.create(
                    email=email,
                    first_name=user_info.get("given_name", ""),
                    last_name=user_info.get("family_name", ""),
                )
                user.set_unusable_password()
                user.save()
            except Exception as e:
                return Response(
                    {"detail": "User not found", "code": "user_not_found"}, status=400
                )

        # Générer un nouveau token JWT pour cet utilisateur avec SimpleJWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = HttpResponseRedirect(f"{settings.FRONTEND_URL}")

        if IN_PROD:
            samesite = "None"
        else:
            samesite = "Lax"

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=IN_PROD,  #  True en production
            samesite=samesite,
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=IN_PROD,
            samesite=samesite,
        )

        return response
