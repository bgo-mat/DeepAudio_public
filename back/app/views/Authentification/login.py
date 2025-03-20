import os
from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from app.serializers import CustomLoginSerializer
from allauth.account.models import EmailAddress
from rest_framework.permissions import AllowAny
from datetime import timedelta
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from deepBack import settings

IN_PROD = settings.IN_PROD


class LoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CustomLoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        remember_me = serializer.validated_data.get("remember_me", False)

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            if not user.is_active:
                return Response(
                    {
                        "detail": "Your account has been deactivated. Please contact support for assistance."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except UserModel.DoesNotExist:
            user = None

        # Authentifie l'utilisateur en utilisant l'email
        user = authenticate(
            request,
            email=email,
            password=password,
        )

        if user is None:
            return Response(
                {
                    "detail": "Invalid credentials. If you believe this is an error, please contact us."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Vérifie que l'email de l'utilisateur est validé
        if not EmailAddress.objects.filter(user=user, verified=True).exists():
            return Response(
                {
                    "detail": "Please verify your email before logging in. If you believe this is an error, please contact us."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Génère les tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Détermine la durée de vie du refresh token selon "remember_me"
        if remember_me:
            refresh.set_exp(lifetime=timedelta(days=30))
        else:
            refresh.set_exp(lifetime=timedelta(days=1))

        response = Response({"detail": "Login successful."}, status=status.HTTP_200_OK)

        if IN_PROD:
            samesite = "None"
        else:
            samesite = "Lax"

        # Définit les cookies pour les tokens
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=IN_PROD,
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


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        email = kwargs.get("email", username)
        if email is None:
            return None
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
