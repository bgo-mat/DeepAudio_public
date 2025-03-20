from rest_framework import serializers
from app.models import Purchase
from app.serializers import PackSerializer, SoundSerializer


class PurchaseSerializer(serializers.ModelSerializer):
    pack = PackSerializer()
    sound = SoundSerializer()

    class Meta:
        model = Purchase
        fields = ["id", "date", "tokens_spent", "pack", "sound"]
