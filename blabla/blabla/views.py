from blabla.blabla.forms import MapForm
from blabla.blabla.models import MapModel
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView, ListView
from django.shortcuts import render, redirect
from registration.models import Profile
from django.contrib.auth.decorators import login_required




class MapFormView(FormView):
    form_class = MapForm
    template_name = "add_routes.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = Profile.objects.get(user=self.request.user)
            form.save()

        return render(request, self.template_name, {'form': form})


@login_required()
def view_routes(request):
    object_list = MapModel.objects.all()
    return render(request, 'view_routes.html', {
        'rides': object_list
    })
