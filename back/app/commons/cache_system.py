from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from functools import partial


class CacheResponseMixin:
    """
    Mixin pour mettre en cache les réponses des vues DRF.
    """

    cache_timeout = 60 * 60  # Temps de cache par défaut en secondes (1 heure)

    def get_cache_key(self, request):
        """
        Génère une clé de cache unique basée sur l'URL et l'utilisateur.
        """
        if request.user.is_authenticated:
            user_id = request.user.id
            cache_key = f"views:{request.path}:user:{user_id}:{request.get_full_path()}"
        else:
            cache_key = f"views:{request.path}:user:anonymous:{request.get_full_path()}"
        return cache_key

    def dispatch(self, request, *args, **kwargs):
        """
        Surcharge la méthode dispatch pour ajouter le mécanisme de cache.
        """
        cache_key = self.get_cache_key(request)
        cached_data = cache.get(cache_key)

        if cached_data:
            # Recréer l'objet Response à partir des données mises en cache
            response = Response()
            response.content = cached_data["content"]
            response.status_code = cached_data["status"]
            response["Content-Type"] = cached_data["content_type"]
            response.accepted_renderer = cached_data.get(
                "accepted_renderer", JSONRenderer()
            )
            response.accepted_media_type = cached_data.get(
                "accepted_media_type", "application/json"
            )
            response.renderer_context = {}  # Vous pouvez ajouter le contexte si nécessaire
            return response

        # Appeler la méthode parent pour obtenir la réponse
        response = super().dispatch(request, *args, **kwargs)

        if isinstance(response, Response):
            response.render()  # Assure que la réponse est rendue et que les attributs sont définis
            # Stocker les données essentielles dans le cache
            cache.set(
                cache_key,
                {
                    "content": response.content,
                    "status": response.status_code,
                    "content_type": response["Content-Type"],
                    "accepted_renderer": response.accepted_renderer,
                    "accepted_media_type": response.accepted_media_type,
                },
                self.cache_timeout,
            )

        return response
