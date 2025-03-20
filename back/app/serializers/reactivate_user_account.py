from rest_framework import serializers
from app.models import User


class AccountReactivationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            if user.is_active:
                raise serializers.ValidationError("Votre compte est déjà actif.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Aucun compte associé à cet email.")
        return value
