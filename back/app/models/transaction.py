from django.db import models
from django.conf import settings
from app.models.subscription_plan import SubscriptionPlan


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("subscription", "Subscription"),
        ("one_time", "One-Time"),
        # Ajouter d'autres types si nécessaire
    )

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("succeeded", "Succeeded"),
        ("failed", "Failed"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="transactions", on_delete=models.CASCADE
    )
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    payment_method = models.CharField(
        max_length=50,
        choices=(("stripe", "Stripe"),),
    )
    transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.email} - {self.amount}€ - {self.get_status_display()}"
