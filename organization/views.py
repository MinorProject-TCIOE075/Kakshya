from django import views
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse_lazy, reverse
from django.views import generic as generic_views

from .forms import DepartmentForm, EditDepartmentForm
from .models import Department, Program


class DepartmentListView(generic_views.TemplateView):
    template_name = 'organization/department_list.html'

    def get_context_data(self, **kwargs):
        departments = Department.objects.all()
        kwargs['departments'] = departments
        return super().get_context_data(**kwargs)


class DepartmentView(views.View):
    form_class = DepartmentForm

    # this should render a new department
    def get(self, request, pk, *args, **kwargs):
        department = get_object_or_404(Department, pk=pk)
        programs = Program.objects.filter(department=department)
        # programs = {}
        context = {"department": department,
                   "programs": programs}
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


def delete_department(request,pk, *args, **kwargs):
    pass
