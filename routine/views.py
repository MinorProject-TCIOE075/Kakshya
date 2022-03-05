from django import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic as generic_views

from .forms import DailyRoutineForm, CourseForm
from .models import DailyRoutine, RoutineCourse


class ListRoutineView(LoginRequiredMixin, PermissionRequiredMixin,
                      generic_views.ListView):
    template_name = 'routine/routine_list.html'
    model = DailyRoutine
    queryset = DailyRoutine.objects.all()
    context_object_name = 'routines'
    permission_required = 'routine.view_routine'
    raise_exception = True


class AddRoutineView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    form_class = DailyRoutineForm
    template_name = 'routine/routine_add.html'
    model = DailyRoutine
    permission_required = 'routine.add_routine'
    raise_exception = True

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


class DetailRoutineView(LoginRequiredMixin, PermissionRequiredMixin,
                        views.View):
    model = DailyRoutine
    template_name = 'routine/routine.html'
    permission_required = (
        'routine.view_routine', 'routine_course.view_routine_course')
    raise_exception = True

    def get(self, request, pk, *args, **kwargs):
        routine = get_object_or_404(self.model, pk=pk)
        routine_courses = routine.courses.all().order_by('start_time')
        message = None
        is_routine_course_deleted = request.GET.get('delete_routine_course',
                                                    None)

        if is_routine_course_deleted:
            message = "Course deleted successfully"

        return render(request, self.template_name,
                      {'routine': routine, 'courses': routine_courses,
                       'message': message})


class EditRoutineView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    form_class = DailyRoutineForm
    template_name = 'routine/routine_edit.html'
    model = DailyRoutine
    raise_exception = True
    permission_required = 'routine.change_routine'

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


@login_required
@permission_required('routine.delete_routine', raise_exception=True)
def delete_routine(request, pk, *args, **kwargs):
    if request.method == 'POST':
        routine = get_object_or_404(DailyRoutine, pk=pk)
        routine.delete()
        return redirect(reverse('myadmin:routine_list'))

    return redirect(reverse('myadmin:routine_list'))


class AddRoutineCourseView(LoginRequiredMixin, PermissionRequiredMixin,
                           views.View):
    form_class = CourseForm
    template_name = 'routine/routine_course_add.html'
    model = RoutineCourse
    permission_required = 'routine_course.add_routine_course'
    raise_exception = True

    def get(self, request, pk, *args, **kwargs):
        routine = get_object_or_404(DailyRoutine, pk=pk)
        routine_course_form = self.form_class(initial={
            'daily_routine': routine
        })
        return render(request, self.template_name,
                      {'routine_course_form': routine_course_form})

    def post(self, request, pk, *args, **kwargs):
        routine_course_form = self.form_class(request.POST)
        if routine_course_form.is_valid():
            routine_course = routine_course_form.save()
            return redirect(reverse('myadmin:routine', kwargs={
                'pk': pk
            }))

        return render(request, self.template_name,
                      {'routine_course_form': routine_course_form})


# Edit Routine Course
class EditRoutineCourseView(LoginRequiredMixin, PermissionRequiredMixin,
                            views.View):
    form_class = CourseForm
    template_name = 'routine/routine_course_edit.html'
    model = RoutineCourse
    permission_required = 'routine_course.change_routine_course'
    raise_exception = True

    def get(self, request, routine_pk, pk, *args, **kwargs):
        routine_course = get_object_or_404(self.model,
                                           daily_routine__pk=routine_pk,
                                           pk=pk)
        routine_course_form = self.form_class(instance=routine_course)

        return render(request, self.template_name,
                      {'routine_course_form': routine_course_form})

    def post(self, request, routine_pk, pk, *args, **kwargs):
        routine_course = get_object_or_404(self.model,
                                           daily_routine__pk=routine_pk, pk=pk)
        routine_course_form = self.form_class(data=request.POST,
                                              instance=routine_course)

        if routine_course_form.is_valid():
            routine_course_form.save()
            return redirect(reverse('myadmin:routine', kwargs={
                'pk': routine_pk
            }))

        return render(request, self.template_name,
                      {'routine_course_form': routine_course_form})


@login_required
@permission_required('routine_course.delete_routine_course')
def delete_routine_course(request, routine_pk, pk, *args, **kwargs):
    if request.method == 'POST':
        routine_course = get_object_or_404(RoutineCourse,
                                           daily_routine__pk=routine_pk, pk=pk)
        routine_course.delete()
        return redirect(reverse('myadmin:routine', kwargs={
            'pk': routine_pk
        }) + '?delete_routine_course=1')

    return redirect(reverse('myadmin:routine', kwargs={
        'pk': routine_pk
    }))
