from django.contrib.postgres.search import SearchVector, SearchQuery
from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import Pack, Sound
from app.serializers import PackSerializer, SoundSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import AllowAny


#
# DOCUMENTATION SWAGGER :
#


@extend_schema_view(
    get=extend_schema(
        description="Requête de search bar<br><br>"
        "La requête cherche des résultats dans : <br>"
        "-Les pack, avec les champs : 'name', 'genres__name', 'description'<br>"
        "-Les sound, avec les champs : 'name', 'type__name', 'subtype__name', 'genres__name', 'bpm', 'key'<br><br>"
        "Exemple de requête avec une phrase (cherche dans le champs 'description') : "
        " http://api-ip/api/search/?q=collection of House music sounds <br><br>"
        "Exemple de requête avec mot clés : "
        "http://localhost:8000/api/search/?q=house 128 c ( cherche dans le genre house, 128bpm, key C"
    ),
)
class SearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get("q", "")
        keywords = query.split()

        # Initialisation des QuerySets vides pour les résultats combinés
        all_packs = Pack.objects.none()
        all_sounds = Sound.objects.none()

        # Étape 1 : Recherche avec la phrase complète
        search_phrase = " ".join(keywords)
        search_query = SearchQuery(search_phrase)

        packs = (
            Pack.objects.annotate(
                search=SearchVector(
                    "name",
                    "genres__name",
                    "description",
                    "sounds__name",
                    "sounds__subtype__name",
                    "sounds__type__name",
                )
            )
            .filter(search=search_query)
            .distinct("id")
        )

        sounds = (
            Sound.objects.annotate(
                search=SearchVector(
                    "name", "type__name", "subtype__name", "genres__name", "bpm", "key"
                )
            )
            .filter(search=search_query)
            .distinct("id")
        )

        # Ajoute les résultats à all_packs et all_sounds
        all_packs = all_packs.union(packs)
        all_sounds = all_sounds.union(sounds)

        # Étape 2 : Recherche itérative (enlever un mot à chaque fois)
        for i in range(len(keywords) - 1, 0, -1):
            search_phrase = " ".join(keywords[:i])
            search_query = SearchQuery(search_phrase)

            packs = (
                Pack.objects.annotate(
                    search=SearchVector(
                        "name",
                        "genres__name",
                        "description",
                        "sounds__name",
                        "sounds__subtype__name",
                        "sounds__type__name",
                    )
                )
                .filter(search=search_query)
                .distinct("id")
            )

            sounds = (
                Sound.objects.annotate(
                    search=SearchVector(
                        "name",
                        "type__name",
                        "subtype__name",
                        "genres__name",
                        "bpm",
                        "key",
                    )
                )
                .filter(search=search_query)
                .distinct("id")
            )

            # Union pour éviter les doublons
            all_packs = all_packs.union(packs)
            all_sounds = all_sounds.union(sounds)

        # Étape 3 : Recherche par mot clé individuel
        for keyword in keywords:
            search_query = SearchQuery(keyword)

            packs = (
                Pack.objects.annotate(
                    search=SearchVector(
                        "name",
                        "genres__name",
                        "description",
                        "sounds__name",
                        "sounds__subtype__name",
                        "sounds__type__name",
                    )
                )
                .filter(search=search_query)
                .distinct("id")
            )

            sounds = (
                Sound.objects.annotate(
                    search=SearchVector(
                        "name",
                        "type__name",
                        "subtype__name",
                        "genres__name",
                        "bpm",
                        "key",
                    )
                )
                .filter(search=search_query)
                .distinct("id")
            )

            # Union des résultats finaux
            all_packs = all_packs.union(packs)
            all_sounds = all_sounds.union(sounds)

        # Sérialisation des résultats
        pack_serializer = PackSerializer(all_packs, many=True)
        sound_serializer = SoundSerializer(all_sounds, many=True)

        return Response(
            {"packs": pack_serializer.data, "sounds": sound_serializer.data}
        )
