from django.db import models
from app.models.user import User
from app.models.pack import Pack
from app.models.sound import Sound


class Purchase(models.Model):
    user = models.ForeignKey(User, related_name="purchases", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    pack = models.ForeignKey(Pack, null=True, blank=True, on_delete=models.SET_NULL)
    sound = models.ForeignKey(Sound, null=True, blank=True, on_delete=models.SET_NULL)
    tokens_spent = models.PositiveIntegerField()

    def __str__(self):
        item = self.pack if self.pack else self.sound
        return f"Achat {self.id} - {self.user.email} - {item.name}"
