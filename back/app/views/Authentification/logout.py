import os

from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

IN_PROD = os.getenv("IN_PROD", "True") == "True"


class LogoutViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response(
                {"detail": "Refresh token non fourni."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = Response(
            {"detail": "Déconnexion réussie."}, status=status.HTTP_200_OK
        )

        # Supprime les cookies en les remplaçant par des valeurs vides et en définissant un expiration passée
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
