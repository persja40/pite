from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blabla.blabla.models import MapModel, SearchModel
from django_google_maps.widgets import GoogleMapsAddressWidget

class MapForm(forms.ModelForm):
    class Meta(object):
        model = MapModel
        fields = ['passengers_number', 'price', 'date', 'hour', 'address_start', 'address_end', 'waypoints',
                  'address_start_lat', 'address_start_lng', 'address_end_lat', 'address_end_lng']
        widgets = {
            "address_end": GoogleMapsAddressWidget,
            "address_start_lat": forms.HiddenInput(),
            "address_start_lng": forms.HiddenInput(),
            "address_end_lat": forms.HiddenInput(),
            "address_end_lng": forms.HiddenInput(),
            "waypoints": forms.HiddenInput()
        }


class SearchForm(forms.ModelForm):
    class Meta(object):
        model = SearchModel
        fields = ['address_start', 'address_end', 'address_start_lat', 'address_start_lng', 'address_end_lat', 'address_end_lng']
        widgets = {
            "address_end": GoogleMapsAddressWidget,
            "address_start_lat": forms.HiddenInput(),
            "address_start_lng": forms.HiddenInput(),
            "address_end_lat": forms.HiddenInput(),
            "address_end_lng": forms.HiddenInput()
        }
