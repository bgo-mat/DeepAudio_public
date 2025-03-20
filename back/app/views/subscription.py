from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, mixins
from app.models import Subscription
from app.serializers import SubscriptionSerializer


class SubscriptionViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
