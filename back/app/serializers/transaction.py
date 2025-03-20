from rest_framework import serializers
from app.models.transaction import Transaction
from app.models.subscription_plan import SubscriptionPlan


class TransactionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    plan_name = serializers.CharField(source="plan.__str__", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "user",
            "user_email",
            "plan",
            "plan_name",
            "date",
            "amount",
            "transaction_type",
            "payment_method",
            "transaction_id",
            "status",
        ]
        read_only_fields = [
            "id",
            "user",
            "user_email",
            "plan_name",
            "date",
            "transaction_id",
            "status",
        ]
