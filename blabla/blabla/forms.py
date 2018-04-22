from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blabla.blabla.models import MapModel
from django_google_maps.widgets import GoogleMapsAddressWidget

class MapForm(forms.ModelForm):

    class Meta(object):
        model = MapModel
        fields = ['address_start', 'address_end', 'waypoints']
        widgets = {
            "address_end": GoogleMapsAddressWidget,
            "waypoints": forms.HiddenInput()
        }
