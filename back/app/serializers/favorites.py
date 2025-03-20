from rest_framework import serializers
from app.models import Sound, Pack


class FavoriteSerializer(serializers.Serializer):
    sound_id = serializers.IntegerField(required=False)
    pack_id = serializers.IntegerField(required=False)

    def validate(self, data):
        if not data.get("sound_id") and not data.get("pack_id"):
            raise serializers.ValidationError(
                "Vous devez fournir un sound_id ou un pack_id."
            )

        if data.get("sound_id"):
            if not Sound.objects.filter(id=data["sound_id"]).exists():
                raise serializers.ValidationError("Le son spécifié n'existe pas.")

        if data.get("pack_id"):
            if not Pack.objects.filter(id=data["pack_id"]).exists():
                raise serializers.ValidationError("Le pack spécifié n'existe pas.")

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        if "sound_id" in validated_data:
            sound = Sound.objects.get(id=validated_data["sound_id"])
            user.favorite_sounds.add(sound)
        if "pack_id" in validated_data:
            pack = Pack.objects.get(id=validated_data["pack_id"])
            user.favorite_packs.add(pack)
        return validated_data

    def delete(self, validated_data):
        user = self.context["request"].user
        if "sound_id" in validated_data:
            sound = Sound.objects.get(id=validated_data["sound_id"])
            user.favorite_sounds.remove(sound)
        if "pack_id" in validated_data:
            pack = Pack.objects.get(id=validated_data["pack_id"])
            user.favorite_packs.remove(pack)
        return validated_data
