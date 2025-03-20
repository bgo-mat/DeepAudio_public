from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from django.urls import reverse
from django.contrib.auth import get_user_model
from app.serializers import CustomSignupSerializer
from rest_framework.permissions import AllowAny
from app.tasks import envoyer_email_verification
from allauth.account.models import EmailAddress, EmailConfirmation

from deepBack import settings

User = get_user_model()
FRONTEND_URL = settings.FRONTEND_URL


class SignupViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CustomSignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        request.data["username"] = None
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save(request)

        # Créer un EmailAddress non vérifié
        email_address = EmailAddress.objects.create(
            user=user,
            email=user.email,
            primary=True,
            verified=False,
        )

        # Créer une confirmation d'e-mail
        email_confirmation = EmailConfirmation.create(email_address)

        # Générer l'URL d'activation
        activation_url = request.build_absolute_uri(
            reverse("auth_confirm_email", args=[email_confirmation.key])
        )

        # Préparer le contexte pour l'e-mail
        context = {
            "user_email": user.email,
            "email_confirmation_key": email_confirmation.key,
            "activation_url": activation_url,
            "site_url": FRONTEND_URL,
        }

        # Envoyer l'e-mail via la tâche Celery
        envoyer_email_verification(context)

        return Response(
            {
                "detail": "Registration successful. Please check your email to confirm your registration."
            },
            status=status.HTTP_201_CREATED,
        )
