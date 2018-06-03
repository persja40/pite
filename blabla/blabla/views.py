from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from blabla.blabla.forms import MapForm, SearchForm
from django.views.generic import FormView
from django.shortcuts import render, get_object_or_404, redirect

from blabla.blabla.models import MapModel, SearchModel
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
            range_meters = float(request.POST.get('range'))
            range_degress = range_meters/111.111
            routes = MapModel.objects.filter(
                address_start_lat__range=(address_start_lat - range_degress, address_start_lat + range_degress),
                address_start_lng__range=(address_start_lng - range_degress, address_start_lng + range_degress),
                address_end_lat__range=(address_end_lat - range_degress, address_end_lat + range_degress),
                address_end_lng__range=(address_end_lng - range_degress, address_end_lng + range_degress))\
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
                route.save()
                search = SearchModel(user=User.objects.get(username=self.request.user))
                search.save()
                search.route_id.add(route_id)
                search.save()
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


@login_required()
def view_signed_routes(request):
    rides = SearchModel.objects.filter(user=request.user)
    signed_ids = list(rides.values_list('id', flat=True))
    rides_ids = list(rides.values_list('route_id', flat=True))
    object_resultset = MapModel.objects.filter(id__in=rides_ids)

    print(rides)
    print(rides_ids)
    print(object_resultset)

    joined = []
    object_list = list(object_resultset.values())

    for signed_id, elem in zip(signed_ids, object_list):
        elem['signed_id'] = signed_id
        joined.append(elem)

    return render(request, 'view_signed_routes.html', {
        'rides': joined
    })


@login_required()
def sign_off_route(request, route_id, signed_id):
    route = MapModel.objects.get(id=route_id)
    passengers_number = route.passengers_signed
    route.passengers_signed = passengers_number - 1
    route.save()

    object_to_delete = get_object_or_404(SearchModel, pk=signed_id)
    object_to_delete.delete()
    return redirect('/view_signed_routes')
