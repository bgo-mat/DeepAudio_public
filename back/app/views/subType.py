from rest_framework.viewsets import GenericViewSet, mixins
from app.models import SubType
from app.serializers import SubTypeSerializer
from rest_framework.permissions import AllowAny


class SubTypeViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = SubTypeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return SubType.objects.all()
