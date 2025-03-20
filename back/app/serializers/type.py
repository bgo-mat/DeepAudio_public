from rest_framework import serializers
from app.models import Type
from app.serializers.subType import SubTypeSerializer


class TypeSerializer(serializers.ModelSerializer):
    sound_count = serializers.IntegerField(source="sounds.count", read_only=True)
    subtypes = SubTypeSerializer(many=True)

    class Meta:
        model = Type
        fields = ["id", "name", "sound_count", "subtypes"]
