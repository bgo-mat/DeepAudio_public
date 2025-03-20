from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAuthenticated
from app.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from app.serializers import NewsletterSubscriptionSerializer


class NewsletterSubscriptionView(GenericViewSet):
    serializer_class = NewsletterSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["patch"], url_path="", url_name="update_newsletter")
    def update_newsletter(self, request):
        """
        Met à jour l'abonnement à la newsletter pour l'utilisateur authentifié.
        """
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Subscription preference updated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
