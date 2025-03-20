import os

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny
from deepBack import settings

IN_PROD = settings.IN_PROD

#
# DOCUMENTATION SWAGGER :
#


@extend_schema_view(
    post=extend_schema(
        description="Cet requête ne nécessite pas de body car le refresh_token est envoyé dans le cookie"
    ),
)
class CookieTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,  # Supprime complètement le besoin d'un body
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token") or request.data.get(
            "refresh"
        )

        if not refresh_token:
            return Response(
                {"detail": "Refresh token manquant."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Remplace le refresh token dans la requête pour qu'il soit traité par la vue de base
        request.data["refresh"] = refresh_token

        # méthode de base pour obtenir le nouveau token
        try:
            response = super().post(request, *args, **kwargs)
        except InvalidToken:
            return Response(
                {"detail": "Refresh token invalide ou expiré."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if IN_PROD:
            samesite = "None"
        else:
            samesite = "Lax"

        # Met à jour le token dans le cookie
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data["access"]
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=IN_PROD,  # True en production
                samesite=samesite,
            )

        return response
