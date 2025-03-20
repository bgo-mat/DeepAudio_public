from rest_framework import serializers


class BuySongSerializer(serializers.Serializer):
    sound_id = serializers.IntegerField(
        required=True, help_text="ID de la chanson à acheter"
    )


class BuyPackSerializer(serializers.Serializer):
    pack_id = serializers.IntegerField(required=True, help_text="ID du pack à acheter")


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(help_text="Message de confirmation")
