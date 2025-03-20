from django.db import models
from django.conf import settings
from app.models.subscription_plan import SubscriptionPlan
from datetime import timedelta


class Subscription(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="subscription", on_delete=models.CASCADE
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    next_payment_date = models.DateTimeField(null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=255)
    trial_end = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} - {self.plan}"
