from django.db import models
from django.contrib.postgres.fields import JSONField
from django_google_maps import fields as map_fields
from django.contrib.auth.models import User




class MapModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_start = map_fields.AddressField(max_length=500)
    address_end = map_fields.AddressField(max_length=500)
    waypoints = JSONField()

