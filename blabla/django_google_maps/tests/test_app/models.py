from django.db import models

from blabla.django_google_maps import AddressField, GeoLocationField


class Person(models.Model):
    address = AddressField(max_length=100)
    geolocation = GeoLocationField(blank=True)
