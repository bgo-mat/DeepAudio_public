from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class AccountReactivationToken(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reactivation_tokens"
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(days=1)  # Token valide 1 jour
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at
