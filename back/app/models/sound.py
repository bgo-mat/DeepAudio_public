from django.db import models
from app.models.type import Type
from app.models.subType import SubType
from app.models.pack import Pack
from app.models.genre import Genre
from app.constantes import PackAvaibalityRole


class Sound(models.Model):
    pack = models.ForeignKey(Pack, related_name="sounds", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    key = models.CharField(max_length=10, blank=True, null=True)
    scale = models.CharField(max_length=5, blank=True, null=True)
    bpm = models.PositiveIntegerField(blank=True)
    genres = models.ManyToManyField(Genre)
    type = models.ManyToManyField(Type, related_name="sounds", blank=True)
    subtype = models.ManyToManyField(SubType, related_name="sounds", blank=True)
    audio_file = models.CharField(max_length=500)
    available_for = models.CharField(
        max_length=10, choices=PackAvaibalityRole, default=PackAvaibalityRole.STANDARD
    )
    created_at = models.DateTimeField(editable=False, null=True)
    number_of_downloads = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        # Héritage automatique de la date de création du pack et du champ available_for
        if self.pack:
            self.created_at = self.pack.created_at
            self.available_for = self.pack.available_for
        super(Sound, self).save(*args, **kwargs)

    def increment_downloads(self):
        """Incrémente le téléchargement pour ce son uniquement."""
        self.number_of_downloads += 1
        self.save()

    def __str__(self):
        return self.name
