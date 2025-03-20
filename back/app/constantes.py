from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    PREMIUM = "PREMIUM", _("Premium")
    PLUS = "PLUS", _("Plus")
    STANDARD = "STANDARD", _("Standard")
    VISITOR = "VISITOR", _("Visitor")
    ADMIN = "ADMIN", _("Admin")


class PackAvaibalityRole(models.TextChoices):
    PREMIUM = "PREMIUM", _("Premium")
    PLUS = "PLUS", _("Plus")
    STANDARD = "STANDARD", _("Standard")


class SubscriptionTypes(models.TextChoices):
    STANDARD = "STANDARD", _("Standard")
    PLUS = "PLUS", _("Plus")
    PREMIUM = "PREMIUM", _("Premium")


class PaymentFrequency(models.TextChoices):
    MONTHLY = "MONTHLY", _("Monthly")
    ANNUAL = "ANNUAL", _("Annual")
