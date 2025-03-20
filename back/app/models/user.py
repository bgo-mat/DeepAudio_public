from django.contrib.auth.models import AbstractUser
from django.db import models
from app.constantes import UserRoles
from app.models.sound import Sound
from app.models.pack import Pack


class User(AbstractUser):
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField("email address", unique=True)
    tokens = models.PositiveIntegerField(default=0)
    accept_newsletter = models.BooleanField(default=False)
    roles = models.CharField(
        choices=UserRoles.choices, max_length=30, default=UserRoles.VISITOR
    )
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    # Champs pour les favoris
    favorite_sounds = models.ManyToManyField(
        Sound, related_name="favorited_by_users", blank=True
    )
    favorite_packs = models.ManyToManyField(
        Pack, related_name="favorited_by_users", blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
