from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.decorators import action
from app.models import User, AccountReactivationToken
from rest_framework import status
from app.serializers import UserSerializer, AccountReactivationSerializer
from app.permissions import UserPermission
from rest_framework.response import Response
from django.urls import reverse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from app.tasks import envoyer_email_reactivation
from deepBack import settings
from django.shortcuts import redirect

FRONTEND_URL = settings.FRONTEND_URL


class UserViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(
        detail=False,
        methods=["patch"],
        url_path="",
        url_name="delete-account",
        permission_classes=[IsAuthenticated, UserPermission],
    )
    def delete_user(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.is_active:
                return Response(
                    {"detail": "Le compte est déjà désactivé."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.is_active = False
            user.save()
            return Response(
                {"detail": "Le compte utilisateur a été désactivé avec succès."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountReactivationSendMailViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = AccountReactivationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = User.objects.get(email=email)
        token = AccountReactivationToken.objects.create(user=user)

        # Construire l'URL de réactivation
        reactivation_url = request.build_absolute_uri(
            reverse("reactivate-account", kwargs={"token": str(token.token)})
        )

        # Préparer le contexte pour l'email de réactivation
        context = {
            "user_email": user.email,
            "reactivation_key": token.token,
            "reactivation_url": reactivation_url,
            "site_url": FRONTEND_URL,
        }
        # Envoyer l'email de réactivation via Celery
        envoyer_email_reactivation(context)

        return Response(
            {
                "detail": "Un email de réactivation a été envoyé. Veuillez vérifier votre boîte de réception."
            },
            status=status.HTTP_200_OK,
        )


class ReactivateAccountLinkView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token, format=None):
        try:
            reactivation_token = AccountReactivationToken.objects.get(token=token)
            if reactivation_token.is_expired():
                return Response(
                    {"detail": "Le lien de réactivation a expiré."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user = reactivation_token.user
            user.is_active = True
            user.save()

            # Supprimer tous les tokens de réactivation de cet utilisateur
            AccountReactivationToken.objects.filter(user=user).delete()

            return redirect(f"{FRONTEND_URL}/connexion")
        except AccountReactivationToken.DoesNotExist:
            return redirect(f"{FRONTEND_URL}/connexion")
