from django.db import models
from app.models.genre import Genre
from app.constantes import PackAvaibalityRole


class Pack(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.DurationField(help_text="Durée totale des sons")
    num_sounds = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    genres = models.ManyToManyField(Genre)
    image = models.CharField(max_length=255)
    preview = models.CharField(max_length=500)
    available_for = models.CharField(
        max_length=10, choices=PackAvaibalityRole, default=PackAvaibalityRole.STANDARD
    )
    created_at = models.DateTimeField(auto_now_add=True)
    number_of_downloads = models.PositiveIntegerField(default=0)

    def increment_downloads(self):
        """Incrémente le téléchargement pour le pack et ses sons associés."""
        self.number_of_downloads += 1
        self.save()
        # Incrémente aussi le nombre de téléchargements pour chaque son dans le pack
        for sound in self.sounds.all():
            sound.increment_downloads()

    def __str__(self):
        return self.name
