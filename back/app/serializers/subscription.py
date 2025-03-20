from rest_framework import serializers

from app.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "plan",
            "start_date",
            "next_payment_date",
            "stripe_subscription_id",
            "trial_end",
            "active",
        ]
