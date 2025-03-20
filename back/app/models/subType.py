from django.db import models
from app.models.type import Type


class SubType(models.Model):
    type = models.ForeignKey(Type, related_name="subtypes", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("type", "name")

    def __str__(self):
        return f"{self.type.name} - {self.name}"
