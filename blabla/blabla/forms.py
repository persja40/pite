from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from blabla.models import MapModel
from django_google_maps.widgets import GoogleMapsAddressWidget


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30)
    last_name = forms.CharField(
        max_length=30)
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')
    phone = forms.DecimalField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email','phone', 'password1', 'password2', )

class MapForm(forms.ModelForm):

    class Meta(object):
        model = MapModel
        fields = ['address', 'geolocation']
        widgets = {
            "address": GoogleMapsAddressWidget,
        }
