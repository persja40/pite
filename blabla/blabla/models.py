from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.fields import FloatField, DateField, IntegerField
from django_google_maps import fields as map_fields
from django.contrib.auth.models import User
from datetime import datetime

class MapModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passengers_number = IntegerField(default=1)
    passengers_signed = IntegerField(default=0)
    price = FloatField(default=0.0)
    date = DateField(default=datetime.now())
    hour = IntegerField(default=12)
    address_start = map_fields.AddressField(max_length=500)
    address_end = map_fields.AddressField(max_length=500)
    address_start_lat = FloatField()
    address_start_lng = FloatField()
    address_end_lat = FloatField()
    address_end_lng = FloatField()
    waypoints = JSONField()

class SearchModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route_id = models.ManyToManyField('MapModel')
    # address_start = map_fields.AddressField(max_length=500)
    # address_end = map_fields.AddressField(max_length=500)
    # address_start_lat = FloatField()
    # address_start_lng = FloatField()
    # address_end_lat = FloatField()
    # address_end_lng = FloatField()