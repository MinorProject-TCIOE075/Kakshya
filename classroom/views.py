from django import views
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic as generic_views

from organization.models import Program
from .forms import CreateClassroomForm
from .models import Classroom


class ClassroomList(generic_views.ListView):
    template_name = 'classroom/classroom_list.html'
    context_object_name = 'classrooms'
    model = Classroom


class CreateClassroomView(views.View):
    template_name = 'classroom/classroom_add.html'
    model = Classroom
    form_class = CreateClassroomForm

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


class EditClassroomView(views.View):
    template_name = 'classroom/classroom_edit.html'
    model = Classroom
    form_class = CreateClassroomForm

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
