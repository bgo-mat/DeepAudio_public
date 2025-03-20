from rest_framework import serializers
from app.models import SubType


class SubTypeSerializer(serializers.ModelSerializer):
    sound_count = serializers.IntegerField(source="sounds.count", read_only=True)

    class Meta:
        model = SubType
        fields = ["id", "name", "sound_count"]
