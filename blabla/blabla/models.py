from django.db import models
from django_google_maps import fields as map_fields


class MapModel(models.Model):
    address_start = map_fields.AddressField(max_length=500)
    address_end = map_fields.AddressField(max_length=500)