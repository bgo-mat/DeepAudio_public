from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="genre_images/", blank=True, null=True)

    def __str__(self):
        return self.name
