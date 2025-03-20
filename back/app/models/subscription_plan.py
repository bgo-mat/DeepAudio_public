from django.db import models
from django.utils.translation import gettext_lazy as _


class SubscriptionPlan(models.Model):
    class SubscriptionTypes(models.TextChoices):
        LITE = "LITE", _("Lite")
        PLUS = "PLUS", _("Plus")
        PREMIUM = "PREMIUM", _("Premium")

    class PaymentFrequency(models.TextChoices):
        MONTHLY = "MONTHLY", _("Monthly")
        ANNUAL = "ANNUAL", _("Annual")

    subscription_type = models.CharField(
        max_length=10,
        choices=SubscriptionTypes.choices,
    )
    payment_frequency = models.CharField(
        max_length=10,
        choices=PaymentFrequency.choices,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credits_per_month = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255)
    stripe_prod_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.get_subscription_type_display()} - {self.get_payment_frequency_display()}"

    class Meta:
        unique_together = ("subscription_type", "payment_frequency")
