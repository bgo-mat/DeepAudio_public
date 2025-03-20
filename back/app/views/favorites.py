from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from app.serializers import SoundSerializer, FavoriteSerializer, PackSerializer
from app.models import Sound
from app.commons.pagination import CustomPagination
from django.core.cache import cache
from deepBack import settings
from rest_framework.decorators import action


class FavoriteViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = FavoriteSerializer
    queryset = Sound.objects.none()  # Fournir un queryset par défaut

    def list(self, request):
        user = request.user
        favorite_sounds = user.favorite_sounds.all()
        favorite_packs = user.favorite_packs.all()

        # Pagination des sons favoris
        page = self.paginate_queryset(favorite_sounds)
        if page is not None:
            sounds_serializer = SoundSerializer(
                page, many=True, context={"request": request}
            )
            sounds_data = sounds_serializer.data
            packs_serializer = PackSerializer(
                favorite_packs, many=True, context={"request": request}
            )
            packs_data = [pack.id for pack in favorite_packs]  # IDs uniquement
            response = self.get_paginated_response(
                {"sounds": sounds_data, "packs": packs_data}
            )
        else:
            sounds_serializer = SoundSerializer(
                favorite_sounds, many=True, context={"request": request}
            )
            sounds_data = sounds_serializer.data
            packs_serializer = PackSerializer(
                favorite_packs, many=True, context={"request": request}
            )
            packs_data = [pack.id for pack in favorite_packs]
            response = Response({"sounds": sounds_data, "packs": packs_data})

        return response

    @action(detail=False, methods=["post"], url_path="add")
    def add_favorite(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.invalidate_user_cache(request)
        return Response({"status": "Favori ajouté avec succès."})

    @action(detail=False, methods=["post"], url_path="remove")
    def remove_favorite(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.delete(serializer.validated_data)
        self.invalidate_user_cache(request)
        return Response({"status": "Favori supprimé avec succès."})

    def invalidate_user_cache(self, request):
        if request.user.is_authenticated:
            # Vérifier si le backend de cache est Redis
            if settings.CACHES["default"]["BACKEND"] == "django_redis.cache.RedisCache":
                # Obtenir le client Redis natif
                redis_client = cache.get_client()
                # Liste des chemins à invalider
                paths = [
                    "/api/sound/",
                    "/api/pack/",
                ]  # Ajoutez d'autres endpoints si nécessaire
                keys_to_delete = []
                for path in paths:
                    # Construire le motif de clé
                    pattern = f"views:{path}*:user:{request.user.id}:*"
                    # Utiliser scan_iter pour récupérer les clés correspondantes
                    for key in redis_client.scan_iter(match=pattern):
                        keys_to_delete.append(key)
                if keys_to_delete:
                    # Supprimer les clés en masse
                    redis_client.delete(*keys_to_delete)
