from django.shortcuts import render
from django.views import generic as generic_views
from django import views

from organization.models import Department


# Create your views here.
class AdminDashboard(views.View):
    template_name = 'myadmin/dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
