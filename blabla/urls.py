"""blabla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from registration import views as registration_views
from blabla.blabla import views as core_views

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^add_routes/$', core_views.MapFormView.as_view(), name='add_routes'),
    url(r'^search_routes/$', core_views.SearchFormView.as_view(), name='search_routes'),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^view_routes/$', core_views.view_routes, name='view_routes'),
    url(r'^view_signed_routes/$', core_views.view_signed_routes, name='view_signed_routes'),
    url(r'^(?P<object_id>[0-9]+)/delete_route/$', core_views.delete_route, name='delete_route'),
    url(r'^(?P<route_id>(\d+))/(?P<signed_id>(\d+))/sign_off_route/$', core_views.sign_off_route, name='sign_off_route'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^signup/$', registration_views.signup, name='signup'),
]
