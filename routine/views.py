from django.shortcuts import render
from django import views
from django.views import generic as generic_views

from .models import DailyRoutine


class ListRoutineView(generic_views.ListView):
    template_name = 'routine/routine_list.html'
    model = DailyRoutine
    queryset = DailyRoutine.objects.all()
    context_object_name = 'routines'
