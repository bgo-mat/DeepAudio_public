from rest_framework.viewsets import GenericViewSet, mixins
from app.commons.cache_system import CacheResponseMixin
from app.models import Sound
from app.serializers import SoundSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from app.commons.pagination import CustomPagination
from django.conf import settings
from rest_framework.permissions import AllowAny

cache_minute = settings.CACHE_TTL

#
# DOCUMENTATION SWAGGER :
#


@extend_schema_view(
    list=extend_schema(
        description="Récupère tous les sounds<br><br>"
        "Pour les filtres : http://api-ip/api/sound/?page=1&type=1&subtype=1&genre=1&key=F&bpm=90<br><br>"
        "Pour ordering (plus récent/plus vieux, plus populaire/moins populaire) : http://api-ip/api/sound/?ordering=-created_at,number_of_downloads <br><br>"
        "Mettre '-' devant le nom de l'ordering pour décroissant<br><br>"
        "Exemple de requête final :  http://api-ip/api/sound/?page=1&type=1&subtype=1&genre=1&key=F&bpm=90&ordering=-created_at,number_of_downloads"
    ),
    retrieve=extend_schema(description=""),
    destroy=extend_schema(description=""),
)
class SoundViewSet(
    CacheResponseMixin,
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = SoundSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]
    cache_timeout = 60 * cache_minute

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["view"] = self  # Inclure la vue pour déterminer l'action
        return context

    def get_queryset(self):
        queryset = Sound.objects.all()
        # Récupérer les paramètres de filtre de la requête
        type_id = self.request.query_params.get("type")
        subtype_id = self.request.query_params.get("subtype")
        genre_id = self.request.query_params.get("genre")
        key = self.request.query_params.get("key")
        bpm = self.request.query_params.get("bpm")

        # Construire le filtre dynamique
        if type_id:
            queryset = queryset.filter(type=type_id)
        if subtype_id:
            queryset = queryset.filter(subtype=subtype_id)
        if genre_id:
            queryset = queryset.filter(genres=genre_id)
        if key:
            queryset = queryset.filter(key=key)
        if bpm:
            queryset = queryset.filter(bpm=bpm)

        ordering = self.request.query_params.get("ordering")
        if ordering:
            queryset = queryset.order_by(*ordering.split(","))
        else:
            queryset = queryset.order_by("-created_at")

        # Éliminer les doublons au cas où des packs répondent à plusieurs critères
        return queryset.distinct()
