from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.fields import FloatField, DateField, IntegerField
from django_google_maps import fields as map_fields
from blabla.blabla.fields import IntegerRangeField
from django.contrib.auth.models import User
from datetime import datetime

class MapModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passengers_number = IntegerField(default=1)
    price = FloatField(default=0.0)
    date = DateField(default=datetime.now())
    hour = IntegerRangeField(default=12, min_value=0, max_value=24)
    address_start = map_fields.AddressField(max_length=500)
    address_end = map_fields.AddressField(max_length=500)
    address_start_lat = FloatField()
    address_start_lng = FloatField()
    address_end_lat = FloatField()
    address_end_lng = FloatField()
    waypoints = JSONField()