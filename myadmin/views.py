from django.shortcuts import render
from django.views import View


# Create your views here.
class AdminDashboard(View):
    template_name = 'myadmin/dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
