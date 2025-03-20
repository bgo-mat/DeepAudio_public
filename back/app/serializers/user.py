from rest_framework import serializers
from app.models import User


class UserSerializer(serializers.ModelSerializer):
    accept_newsletter = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "tokens",
            "roles",
            "accept_newsletter",
            "is_active",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        # Utiliser `set_password` pour hacher le mot de passe
        accept_newsletter = validated_data.pop("accept_newsletter", False)
        user = User.objects.create(
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.accept_newsletter = accept_newsletter
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Mise à jour des informations utilisateur, gestion du mot de passe
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.email = validated_data.get("email", instance.email)

        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance
