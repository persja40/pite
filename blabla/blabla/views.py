from blabla.blabla.forms import MapForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from django.shortcuts import render, redirect

class MapFormView(FormView):
    form_class = MapForm
    template_name = "home.html"
