from django.db import models


class WorldCities(models.Model):
    city = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    id = models.TextField(blank=True, primary_key=True)

    class Meta:
        managed = False
        db_table = 'worldcities'
