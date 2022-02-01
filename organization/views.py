from django import views
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse_lazy, reverse
from django.views import generic as generic_views

from .forms import DepartmentForm, EditDepartmentForm, ProgramForm, \
    EditProgramForm
from .models import Department, Program, Course


class DepartmentListView(generic_views.TemplateView):
    template_name = 'organization/department_list.html'

    def get_context_data(self, **kwargs):
        departments = Department.objects.all()
        kwargs['departments'] = departments
        is_department_deleted = self.request.GET.get('deleted_department',
                                                     None)
        message = None
        if is_department_deleted == '1':
            message = 'Department deleted successfully.'

        kwargs['message'] = message

        return super().get_context_data(**kwargs)


class DepartmentView(views.View):
    form_class = DepartmentForm

    # this should render a new department
    def get(self, request, pk, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        programs = Program.objects.filter(department=department)
        # programs = {}
        message = None
        is_program_deleted = request.GET.get('deleted_program')
        if is_program_deleted:
            message = "Program deleted successfully."
        context = {"department": department,
                   "programs": programs, 'message': message}
        return render(request, 'organization/department.html', context)


class AddDepartmentView(views.View):
    model = Department
    form_class = DepartmentForm
    success_url = reverse_lazy('myadmin:department_list')
    template_name = 'organization/add_department.html'

    def get(self, request, *args, **kwargs):
        department_form = self.form_class()
        return render(request, self.template_name,
                      context={'department_form': department_form})

    def post(self, request, *args, **kwargs):
        department_form = self.form_class(request.POST)
        if department_form.is_valid():
            name = department_form.cleaned_data.get('name')
            code = department_form.cleaned_data.get('code')

            department = self.model()
            department.name = name
            department.code = code
            department.created_by = request.user
            department.save()
            return redirect(self.success_url)
        return render(request, self.template_name,
                      context={'department_form': department_form})


class EditDepartmentView(views.View):
    model = Department
    form_class = EditDepartmentForm
    template_name = 'organization/department_edit.html'

    def get(self, request, pk, *args, **kwargs):
        department = get_object_or_404(self.model, pk=pk)

        department_form = self.form_class(initial={
            'name': department.name,
            'code': department.code
        })
        return render(request, self.template_name, {
            "department_form": department_form
        })

    def post(self, request, pk, *args, **kwargs):
        department = get_object_or_404(self.model, pk=pk)

        department_form = self.form_class(request.POST)
        if department_form.is_valid():
            department.name = department_form.cleaned_data.get('name',
                                                               department.name)
            department.code = department_form.cleaned_data.get('code',
                                                               department.code)
            department.save()
            return redirect(reverse('myadmin:department_list'))
        return render(request, self.template_name, {
            "department_form": department_form
        })


def delete_department(request, pk, *args, **kwargs):
    if request.method == "POST":
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return redirect(
            reverse('myadmin:department_list') + '?deleted_department=1')
    return redirect(reverse('myadmin:department', kwargs={'pk': pk}))


# Add program
class AddProgramView(views.View):
    model = Program
    form_class = ProgramForm
    template_name = 'organization/program_add.html'

    def get(self, request, department_pk, *args, **kwargs):
        department = get_object_or_404(Department, pk=department_pk)
        program_form = self.form_class(initial={
            'department': department
        })

        return render(request, self.template_name, context={
            'program_form': program_form,
        })

    def post(self, request, *args, **kwargs):
        program_form = self.form_class(request.POST)
        if program_form.is_valid():
            name = program_form.cleaned_data.get('name', None)
            code = program_form.cleaned_data.get('code', None)
            year = program_form.cleaned_data.get('year', None)
            department = program_form.cleaned_data.get('department', None)

            program = Program()
            program.name = name
            program.code = code
            program.year = year
            program.department = department
            program.created_by = request.user
            program.save()
            return redirect(reverse('myadmin:department', kwargs={
                "pk": department.pk
            }))
        return render(request, self.template_name, context={
            'program_form': program_form,
        })


# Edit program
class EditProgramView(views.View):
    model = Program
    form_class = EditProgramForm
    template_name = 'organization/program_edit.html'

    def get(self, request, pk, *args, **kwargs):
        program = get_object_or_404(self.model, pk=pk)

        program_form = self.form_class(initial={
            'name': program.name,
            'code': program.code,
            'year': program.year,
            'department': program.department
        })
        return render(request, self.template_name, {
            "program_form": program_form
        })

    def post(self, request, department_pk, pk, *args, **kwargs):
        program = get_object_or_404(self.model, pk=pk)

        program_form = self.form_class(request.POST)
        if program_form.is_valid():
            program.name = program_form.cleaned_data.get('name',
                                                         program.name)
            program.code = program_form.cleaned_data.get('code',
                                                         program.code)
            program.year = program_form.cleaned_data.get('year', program.year)
            program.department = program_form.cleaned_data.get('department',
                                                               program.department)
            program.save()
            return redirect(
                reverse('myadmin:department', kwargs={"pk": department_pk}))
        return render(request, self.template_name, {
            "program_form": program_form
        })


# Delete program
def delete_program(request, department_pk, pk, *args, **kwargs):
    if request.method == "POST":
        program = get_object_or_404(Program, pk=pk)
        program.delete()
        return redirect(
            reverse('myadmin:department',
                    kwargs={"pk": department_pk}) + '?deleted_program=1')
    return redirect(reverse('myadmin:department', kwargs={'pk': pk}))


# List Courses
class CourseListView(generic_views.ListView):
    queryset = Course.objects.all()
    template_name = 'organization/course_list.html'
    context_object_name = 'courses'
# View Course
# add course 
# Edit Courses
# delete Course


