from django import views
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic as generic_views

from .forms import DailyRoutineForm
from .models import DailyRoutine


class ListRoutineView(generic_views.ListView):
    template_name = 'routine/routine_list.html'
    model = DailyRoutine
    queryset = DailyRoutine.objects.all()
    context_object_name = 'routines'


class AddRoutineView(views.View):
    form_class = DailyRoutineForm
    template_name = 'routine/routine_add.html'
    model = DailyRoutine

    def get(self, request, *args, **kwargs):
        routine_form = self.form_class()
        return render(request, self.template_name, {
            'routine_form': routine_form
        })

    def post(self, request, *args, **kwargs):
        routine_form = self.form_class(request.POST)

        if routine_form.is_valid():
            routine_form.save()
            return redirect(reverse('myadmin:routine_list'))

        return render(request, self.template_name, {
            'routine_form': routine_form
        })


class DetailRoutineView(views.View):
    model = DailyRoutine
    template_name = 'routine/routine.html'

    def get(self, request, pk, *args, **kwargs):
        routine = get_object_or_404(self.model, pk=pk)
        return render(request, self.template_name, {'routine': routine})


class EditRoutineView(views.View):
    form_class = DailyRoutineForm
    template_name = 'routine/routine_edit.html'
    model = DailyRoutine

    def get(self, request, pk, *args, **kwargs):
        routine = get_object_or_404(self.model, pk=pk)

        routine_form = self.form_class(instance=routine)
        return render(request, self.template_name, {
            'routine_form': routine_form
        })

    def post(self, request, pk, *args, **kwargs):
        routine = get_object_or_404(self.model, pk=pk)
        routine_form = self.form_class(data=request.POST, instance=routine)

        if routine_form.is_valid():
            routine_form.save()
            return redirect(reverse('myadmin:routine', kwargs={"pk": pk}))

        return render(request, self.template_name, {
            'routine_form': routine_form
        })


def delete_routine(request, pk, *args, **kwargs):
    if request.method == 'POST':
        routine = get_object_or_404(DailyRoutine, pk=pk)
        routine.delete()
        return redirect(reverse('myadmin:routine_list'))

    return redirect(reverse('myadmin:routine_list'))
