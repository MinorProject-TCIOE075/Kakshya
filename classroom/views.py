from django.shortcuts import render
from django import views
from django.views import generic as generic_views

from .models import Classroom


class ClassroomList(generic_views.ListView):
    template_name = 'classroom/classroom_list.html'
    context_object_name = 'classrooms'
    model = Classroom
