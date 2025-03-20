from rest_framework import serializers
from app.models import User


class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    accept_newsletter = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ["accept_newsletter"]
