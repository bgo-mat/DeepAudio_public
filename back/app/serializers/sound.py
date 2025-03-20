from rest_framework import serializers

from app.commons.crypto_utils import encrypt_text
from app.models import Sound, Purchase
from datetime import timedelta
from app.serializers.S3_fields import S3Base64FileField, S3Base64ImageField


class SoundSerializer(serializers.ModelSerializer):
    # Write-only fields for input
    type = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    subtype = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    # Read-only fields for output
    type_names = serializers.SerializerMethodField(read_only=True)
    subtype_names = serializers.SerializerMethodField(read_only=True)

    duration_seconds = serializers.FloatField(write_only=True)
    duration = serializers.DurationField(read_only=True)
    audio_file = S3Base64FileField(required=True)
    pack = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    image = S3Base64ImageField(source="pack.image", read_only=True)
    is_favorite = serializers.SerializerMethodField()
    is_buy = serializers.SerializerMethodField()

    class Meta:
        model = Sound
        fields = [
            "id",
            "pack",
            "name",
            "price",
            "key",
            "scale",
            "bpm",
            "duration_seconds",
            "duration",
            "type",
            "type_names",
            "subtype",
            "subtype_names",
            "audio_file",
            "available_for",
            "image",
            "is_favorite",
            "is_buy"
        ]

    def get_is_favorite(self, obj):
        request = self.context.get("request", None)
        if request and request.user and request.user.is_authenticated:
            return request.user.favorite_sounds.filter(id=obj.id).exists()
        return False

    def get_is_buy(self, obj):
        request = self.context.get("request", None)
        if request and request.user and request.user.is_authenticated:
            user = request.user
            print(obj, "icicicic user", flush=True)
            return Purchase.objects.filter(user=user, sound__name=obj).exists()
        return False

    def get_image(self, obj):
        if obj.pack and obj.pack.image:
            return obj.pack.image
        return None

    def get_type_names(self, obj):
        return [type_obj.name for type_obj in obj.type.all()]

    def get_subtype_names(self, obj):
        return [subtype_obj.name for subtype_obj in obj.subtype.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        view = self.context.get("view")
        action = getattr(view, "action", "") if view else ""

        if action in ["retrieve", "list"]:
            audio_file = representation.get("audio_file")
            if audio_file:
                # Chiffrer l'URL ou le contenu du fichier audio
                representation["audio_file"] = encrypt_text(audio_file)

        return representation

    def validate(self, attrs):
        duration_seconds = attrs.pop("duration_seconds", None)
        if duration_seconds is not None:
            attrs["duration"] = timedelta(seconds=duration_seconds)
        else:
            attrs["duration"] = timedelta(seconds=0)
        return attrs
