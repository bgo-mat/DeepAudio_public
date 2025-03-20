from rest_framework.viewsets import GenericViewSet, mixins
from app.models import Genre
from app.serializers import GenreSerializer, GenreSerializerRetrieve
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny

#
# DOCUMENTATION SWAGGER :
#


@extend_schema_view(
    list=extend_schema(description="Récupère tous les genre avec leurs images"),
    retrieve=extend_schema(
        description="Récupère un genre spécifique avec des sons et pack associé au genre<br><br>"
        "Pour les filtres : http://api-ip/api/genre/id/?pack_page=1&sound_page=2"
    ),
    create=extend_schema(description=""),
    update=extend_schema(description=""),
    partial_update=extend_schema(description=""),
    destroy=extend_schema(description=""),
)
class GenreViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Genre.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GenreSerializerRetrieve
        else:
            return GenreSerializer
