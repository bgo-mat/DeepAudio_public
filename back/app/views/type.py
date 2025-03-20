from rest_framework.viewsets import GenericViewSet, mixins
from app.models import Type
from rest_framework.permissions import AllowAny
from app.serializers import TypeSerializer


class TypeViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = TypeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Type.objects.all()
