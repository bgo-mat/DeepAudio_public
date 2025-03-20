from rest_framework.views import APIView
from django.shortcuts import redirect
from allauth.account.models import EmailConfirmation
from rest_framework.permissions import AllowAny

from deepBack import settings

FRONTEND_URL = settings.FRONTEND_URL


class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, key, format=None):
        try:
            email_confirmation = EmailConfirmation.objects.get(key=key)
            email_confirmation.confirm(request)

            return redirect(f"{FRONTEND_URL}/connexion")
        except EmailConfirmation.DoesNotExist:
            return redirect(f"{FRONTEND_URL}/")
