from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from blabla.blabla.forms import MapForm, SearchForm
from django.views.generic import FormView
from django.shortcuts import render, get_object_or_404, redirect

from blabla.blabla.models import MapModel
from registration.models import Profile


# @login_required()
class MapFormView(FormView):
    form_class = MapForm
    template_name = "add_routes.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = User.objects.get(username=self.request.user)
            form.instance.passengers_signed = 0
            form.save()
        return render(request, self.template_name, {'form': form})


# @login_required()
class SearchFormView(FormView):
    form_class = SearchForm
    template_name = "search_routes.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if "search" in request.POST:
            address_start_lat = float(request.POST.get('address_start_lat'))
            address_start_lng = float(request.POST.get('address_start_lng'))
            address_end_lat = float(request.POST.get('address_end_lat'))
            address_end_lng = float(request.POST.get('address_end_lng'))
            routes = MapModel.objects.filter(
                address_start_lat__range=(address_start_lat - 0.1, address_start_lat + 0.1),
                address_start_lng__range=(address_start_lng - 0.1, address_start_lng + 0.1),
                address_end_lat__range=(address_end_lat - 0.1, address_end_lat + 0.1),
                address_end_lng__range=(address_end_lng - 0.1, address_end_lng + 0.1))\
                .exclude(user=request.user)
            return render(request, self.template_name, {'form': form, 'routes': routes})
        elif "sign" in request.POST:
            route_id = float(request.POST.get('route_id'))
            route = MapModel.objects.get(id=route_id)
            passengers_number = route.passengers_number
            passengers_signed = route.passengers_signed
            new_passengers_signed = passengers_signed + 1
            if new_passengers_signed > passengers_number:
                return render(request, self.template_name,
                              {'form': form,
                               'signed_message': "You can't sign for this route. There is already enough number of passengers!"})
            else:
                route.passengers_signed = new_passengers_signed
                return render(request, self.template_name,
                              {'form': form,
                               'signed_message': "You have signed for this route", 'route_details': route})


@login_required()
def view_routes(request):
    object_list = MapModel.objects.filter(user=request.user)
    return render(request, 'view_routes.html', {
        'rides': object_list
    })


@login_required()
def delete_route(request, object_id):
    object_to_delete = get_object_or_404(MapModel, pk=object_id)
    object_to_delete.delete()
    return redirect('/view_routes')
