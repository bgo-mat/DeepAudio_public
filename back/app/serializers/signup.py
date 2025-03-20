from rest_framework import serializers
from allauth.account.adapter import get_adapter
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from deepBack import settings

User = get_user_model()


class CustomSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password", "accept_newsletter")

        # Validation de l'unicité de l'email

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Un utilisateur avec cet email existe déjà."
            )
        return value

    # Validation du mot de passe selon les règles de sécurité Django
    def validate_password(self, value):
        validate_password(
            value
        )  # Utilise les validateurs de mot de passe intégrés de Django
        return value

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.validated_data

        # Validation du mot de passe avant de sauvegarder l'utilisateur
        password = self.cleaned_data.get("password")
        adapter.clean_password(
            password, user=user
        )  # Nettoyage du mot de passe avec allauth

        # Assigner accept_newsletter à l'utilisateur
        accept_newsletter = self.cleaned_data.get("accept_newsletter", False)
        user.accept_newsletter = accept_newsletter

        adapter.save_user(request, user, self)
        if self.validated_data.get("accept_newsletter"):
            user.tokens += settings.FREE_TOKENS
            user.save()

        return user
