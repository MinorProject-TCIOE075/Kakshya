from django import views
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic as generic_views
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.contrib.auth.decorators import login_required, permission_required
from organization.models import Program
from .forms import CreateClassroomForm
from .models import Classroom


class ClassroomList(LoginRequiredMixin, PermissionRequiredMixin, generic_views.ListView):
    template_name = 'classroom/classroom_list.html'
    context_object_name = 'classrooms'
    model = Classroom
    permission_required = 'classroom.view_classroom'
    raise_exception = True


class CreateClassroomView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    template_name = 'classroom/classroom_add.html'
    model = Classroom
    form_class = CreateClassroomForm
    permission_required = 'classroom.add_classroom'
    raise_exception = True

    def get(self, request, department_pk, program_pk, *args, **kwargs):
        program = get_object_or_404(Program, pk=program_pk,
                                    department=department_pk)
        create_classroom_form = self.form_class()
        return render(request, self.template_name,
                      {
                          'classroom_form': create_classroom_form,
                          'program': program
                      })

    def post(self, request, department_pk, program_pk, *args, **kwargs):
        program = get_object_or_404(Program, pk=program_pk,
                                    department=department_pk)
        create_classroom_form = self.form_class(request.POST)
        if create_classroom_form.is_valid():
            classroom = create_classroom_form.save(commit=False)
            classroom.program = program
            classroom.created_by = request.user
            classroom.save()
            return redirect(reverse('myadmin:program', kwargs={
                'department_pk': program.department.pk,
                'pk': program.pk
            }))

        return render(request, self.template_name,
                      {
                          'classroom_form': create_classroom_form,
                          'program': program
                      })


class EditClassroomView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    template_name = 'classroom/classroom_edit.html'
    model = Classroom
    form_class = CreateClassroomForm
    permission_required = 'classroom.change_classroom'
    raise_exception = True

    def get(self, request, department_pk, program_pk, pk, *args, **kwargs):
        program = get_object_or_404(Program, pk=program_pk,
                                    department=department_pk)

        classroom = get_object_or_404(Classroom, pk=pk)

        create_classroom_form = self.form_class(instance=classroom)
        return render(request, self.template_name,
                      {
                          'classroom_form': create_classroom_form,
                          'program': program
                      })

    def post(self, request, department_pk, program_pk, pk, *args, **kwargs):
        program = get_object_or_404(Program, pk=program_pk,
                                    department=department_pk)
        classroom = get_object_or_404(Classroom, pk=pk)

        create_classroom_form = self.form_class(request.POST,
                                                instance=classroom)
        if create_classroom_form.is_valid():
            print(create_classroom_form.cleaned_data)
            create_classroom_form.save()
            return redirect(reverse('myadmin:program', kwargs={
                'department_pk': program.department.pk,
                'pk': program.pk
            }))

        return render(request, self.template_name,
                      {
                          'classroom_form': create_classroom_form,
                          'program': program
                      })


@login_required
@permission_required('classroom.can_archive_classroom', raise_exception=True)
def archive_classroom(request, department_pk, program_pk, pk, *args, **kwargs):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        print("classroom archived")
        classroom.is_archived = True
        classroom.save()
        return redirect(reverse('myadmin:program', kwargs={
            'pk': classroom.program.pk,
            'department_pk': classroom.program.department.pk
        }) + '?archived=1')

    return redirect(reverse('myadmin:program', kwargs={
        'pk': classroom.program.pk,
        'department_pk': classroom.program.department.pk
    }))


@login_required
@permission_required('classroom.can_archive_classroom', raise_exception=True)
def restore_classroom(request, department_pk, program_pk, pk, *args, **kwargs):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        print("classroom restored")
        if classroom.is_archived:
            classroom.is_archived = False
            classroom.save()
        return redirect(reverse('myadmin:program', kwargs={
            'pk': classroom.program.pk,
            'department_pk': classroom.program.department.pk
        }) + '?restored=1')

    return redirect(reverse('myadmin:program', kwargs={
        'pk': classroom.program.pk,
        'department_pk': classroom.program.department.pk
    }))


def delete_classroom(request, department_pk, program_pk, pk, *args, **kwargs):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        print("classroom deleted")
        classroom.delete()
        return redirect(reverse('myadmin:program', kwargs={
            'pk': classroom.program.pk,
            'department_pk': classroom.program.department.pk
        }) + '?classroom_deleted=1')

    return redirect(reverse('myadmin:program', kwargs={
        'pk': classroom.program.pk,
        'department_pk': classroom.program.department.pk
    }))
