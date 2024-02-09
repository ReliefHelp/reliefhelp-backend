from django.db import models

# Create your models here.


class Earthquake(models.Model):
    place = models.CharField(max_length=255)
    time = models.DateTimeField()
    magnitude = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.place
