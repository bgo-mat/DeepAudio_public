from rest_framework import serializers

from app.commons.pagination import CustomPagination
from app.models import Pack, Genre, Type, SubType, Sound
from app.serializers.S3_fields import S3Base64FileField, S3Base64ImageField
from app.serializers.sound import SoundSerializer
import re
from datetime import timedelta


def parse_duration_string(duration_str):
    pattern = r"(?:(?P<minutes>\d+)min)?(?:(?P<seconds>\d+)s)?"
    match = re.match(pattern, duration_str)
    if not match:
        return timedelta()
    minutes = int(match.group("minutes") or 0)
    seconds = int(match.group("seconds") or 0)
    return timedelta(minutes=minutes, seconds=seconds)


class PackSerializer(serializers.ModelSerializer):
    # Write-only field for input
    genres = serializers.ListField(child=serializers.CharField(), write_only=True)

    # Read-only field for output
    labels = serializers.SerializerMethodField(read_only=True)
    genre_names = serializers.SerializerMethodField(read_only=True)
    sounds = SoundSerializer(many=True, write_only=True)
    total_duration = serializers.CharField(write_only=True)
    duration = serializers.DurationField(read_only=True)
    image = S3Base64ImageField(required=True)
    num_sounds = serializers.IntegerField(read_only=True)
    preview = S3Base64FileField(required=True)
    is_favorite = serializers.SerializerMethodField()
    paginated_sounds = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pack
        fields = [
            "id",
            "name",
            "description",
            "total_duration",
            "duration",
            "num_sounds",
            "price",
            "genres",
            "genre_names",
            "labels",
            "image",
            "available_for",
            "preview",
            "is_favorite",
            "sounds",
            "paginated_sounds"
        ]

    def get_is_favorite(self, obj):
        request = self.context.get("request", None)
        if request and request.user and request.user.is_authenticated:
            return request.user.favorite_sounds.filter(id=obj.id).exists()
        return False

    def get_labels(self, obj):
        labels = set()

        # Ajouter les genres du pack
        for genre in obj.genres.all():
            labels.add(genre.name)

        # Ajouter les types et sous-types des sons
        for sound in obj.sounds.all():
            for type_obj in sound.type.all():
                labels.add(type_obj.name)
            for subtype_obj in sound.subtype.all():
                labels.add(subtype_obj.name)

        return list(labels)

    def get_genre_names(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def create(self, validated_data):
        sounds_data = validated_data.pop("sounds")
        genres_data = validated_data.pop("genres")
        total_duration_str = validated_data.pop("total_duration", None)

        # Convert total_duration to timedelta
        if total_duration_str:
            duration = parse_duration_string(total_duration_str)
            validated_data["duration"] = duration

        # Set num_sounds
        validated_data["num_sounds"] = len(sounds_data)

        pack = Pack.objects.create(**validated_data)

        # Handle genres
        pack_genres = []
        for genre_name in genres_data:
            genre, _ = Genre.objects.get_or_create(name=genre_name)
            pack_genres.append(genre)
        pack.genres.set(pack_genres)

        # Handle sounds
        for sound_data in sounds_data:
            type_names = sound_data.pop("type", [])
            subtype_names = sound_data.pop("subtype", [])

            sound = Sound.objects.create(pack=pack, **sound_data)

            # Assign pack genres to sound
            sound.genres.set(pack_genres)

            # Handle types
            sound_types = []
            for type_name in type_names:
                type_obj, _ = Type.objects.get_or_create(name=type_name)
                sound_types.append(type_obj)
            sound.type.set(sound_types)

            # Handle subtypes
            sound_subtypes = []
            for subtype_name in subtype_names:
                subtype_obj = SubType.objects.filter(name=subtype_name).first()
                if not subtype_obj:
                    if sound_types:
                        subtype_obj, _ = SubType.objects.get_or_create(
                            name=subtype_name, type=sound_types[0]
                        )
                    else:
                        raise serializers.ValidationError(
                            f"Cannot create subtype '{subtype_name}' without an associated type."
                        )
                sound_subtypes.append(subtype_obj)
            sound.subtype.set(sound_subtypes)

        return pack

    def get_paginated_sounds(self, obj):
        request = self.context.get("request")
        if not request:
            return SoundSerializer(obj.sounds.all(), many=True).data

        # Utiliser un paginator personnalisé si nécessaire
        paginator = CustomPagination()
        # Récupérer le paramètre de page spécifique aux sons, par exemple 'sounds_page'
        sounds_page = request.query_params.get("sounds_page", 1)
        paginator.page_size = (
            10
        )

        # Paginator manuellement les sons
        sounds_qs = obj.sounds.all()
        paginated_sounds = paginator.paginate_queryset(sounds_qs, request)
        serializer = SoundSerializer(paginated_sounds, many=True, context=self.context)

        return paginator.get_paginated_response(serializer.data).data
