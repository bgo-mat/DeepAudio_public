from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import Sound, Purchase, Pack
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from app.serializers import BuyPackSerializer, BuySongSerializer, MessageSerializer
from drf_spectacular.utils import extend_schema


class BuySongView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BuySongSerializer,
        responses={201: MessageSerializer, 400: MessageSerializer},
        description="Acheter une chanson spécifique en fournissant son ID.",
    )
    def post(self, request):
        serializer = BuySongSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        sound_id = request.data.get("sound_id")

        if not sound_id:
            return Response(
                {"error": "L'ID de la chanson est requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sound = get_object_or_404(Sound, id=sound_id)

        # Vérifier si l'utilisateur a déjà acheté cette chanson
        if Purchase.objects.filter(user=user, sound=sound).exists():
            return Response(
                {"error": "Vous avez déjà acheté cette chanson."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Vérifier si l'utilisateur a suffisamment de jetons
        tokens_needed = int(sound.price)
        if user.tokens < tokens_needed:
            return Response(
                {"error": "Fonds insuffisants."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Déduire les jetons
        user.tokens -= tokens_needed
        user.save()

        # Créer un enregistrement d'achat
        Purchase.objects.create(user=user, sound=sound, tokens_spent=tokens_needed)

        # Incrémenter le nombre de téléchargements
        sound.increment_downloads()

        return Response(
            {"message": "Chanson achetée avec succès."}, status=status.HTTP_201_CREATED
        )


class BuyPackView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=BuyPackSerializer,
        responses={201: MessageSerializer, 400: MessageSerializer},
        description="Acheter un pack spécifique en fournissant son ID. Inclut tous les sons du pack dans l'achat.",
    )
    def post(self, request):
        serializer = BuyPackSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        pack_id = request.data.get("pack_id")

        if not pack_id:
            return Response(
                {"error": "L'ID du pack est requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        pack = get_object_or_404(Pack, id=pack_id)

        # Vérifier si l'utilisateur a déjà acheté ce pack
        if Purchase.objects.filter(user=user, pack=pack).exists():
            return Response(
                {"error": "Vous avez déjà acheté ce pack."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Vérifier si l'utilisateur a suffisamment de jetons
        tokens_needed = int(pack.price)
        if user.tokens < tokens_needed:
            return Response(
                {"error": "Fonds insuffisants."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Déduire les jetons
        user.tokens -= tokens_needed
        user.save()

        # Créer un enregistrement d'achat pour le pack
        Purchase.objects.create(user=user, pack=pack, tokens_spent=tokens_needed)

        # Créer des enregistrements d'achat pour chaque son du pack
        sounds = pack.sounds.all()
        for sound in sounds:
            # Vérifier si l'utilisateur a déjà acheté ce son
            if not Purchase.objects.filter(user=user, sound=sound).exists():
                Purchase.objects.create(
                    user=user,
                    sound=sound,
                    tokens_spent=0,  # Puisque l'utilisateur a payé pour le pack
                )
                # Incrémenter le nombre de téléchargements pour chaque son
                sound.increment_downloads()

        # Incrémenter le nombre de téléchargements du pack
        pack.increment_downloads()

        return Response(
            {"message": "Pack acheté avec succès."}, status=status.HTTP_201_CREATED
        )
