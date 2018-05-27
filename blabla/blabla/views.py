from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from blabla.blabla.forms import MapForm
from django.views.generic import FormView
from django.shortcuts import render, get_object_or_404, redirect

from blabla.blabla.models import MapModel
from registration.models import Profile


class MapFormView(FormView):
    form_class = MapForm
    template_name = "add_routes.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = User.objects.get(username=self.request.user)
            form.save()

        return render(request, self.template_name, {'form': form})


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
