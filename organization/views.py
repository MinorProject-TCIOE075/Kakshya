from django import views
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (PermissionRequiredMixin,
                                        LoginRequiredMixin)
from django.shortcuts import render, get_object_or_404, redirect
from django.urls.base import reverse_lazy, reverse
from django.views import generic as generic_views

from classroom.models import Classroom
from .forms import (DepartmentForm, EditDepartmentForm, ProgramForm,
                    EditProgramForm, CourseForm, AddUsersToProgramForm)
from .models import Department, Program, Course

User = get_user_model()


class DepartmentListView(LoginRequiredMixin, PermissionRequiredMixin,
                         generic_views.TemplateView):
    permission_required = ('department.view_department',)
    template_name = 'organization/department_list.html'
    raise_exception = True

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


class DepartmentView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    form_class = DepartmentForm
    raise_exception = True
    permission_required = ('department.view_department', 'program.view_program')

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


class AddDepartmentView(LoginRequiredMixin, PermissionRequiredMixin,
                        views.View):
    model = Department
    form_class = DepartmentForm
    success_url = reverse_lazy('myadmin:department_list')
    template_name = 'organization/add_department.html'
    permission_required = ('department.add_department',)
    raise_exception = True

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


class EditDepartmentView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    model = Department
    form_class = EditDepartmentForm
    template_name = 'organization/department_edit.html'
    permission_required = 'department.change_department'
    raise_exception = True

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


@login_required
@permission_required('department.delete_department', raise_exception=True)
def delete_department(request, pk, *args, **kwargs):
    if request.method == "POST":
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return redirect(
            reverse('myadmin:department_list') + '?deleted_department=1')
    return redirect(reverse('myadmin:department', kwargs={'pk': pk}))


class ProgramDetailView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    template_name = 'organization/program.html'
    model = Program
    permission_required = ('program.view_program', 'classroom.view_classroom')
    raise_exception = True

    def get(self, request, department_pk, pk, *args, **kwargs):
        program = get_object_or_404(self.model, pk=pk,
                                    department__pk=department_pk)
        classrooms = Classroom.objects.filter(program=program)

        message = ''
        is_archived = request.GET.get('archived', None)
        is_restored = request.GET.get('restored', None)
        is_classroom_deleted = request.GET.get('classroom_deleted', None)
        if is_archived == '1':
            message = "Classroom archived successfully!"
        if is_restored == "1":
            message = "Classroom restored successfully!"
        if is_classroom_deleted == '1':
            message = "Classroom deleted successfully!"
        return render(request, self.template_name, {'program': program,
                                                    'classrooms': classrooms,
                                                    'message': message})


# Add program
class AddProgramView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    model = Program
    form_class = ProgramForm
    template_name = 'organization/program_add.html'
    permission_required = 'program.add_program'
    raise_exception = True

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
class EditProgramView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    model = Program
    form_class = EditProgramForm
    template_name = 'organization/program_edit.html'
    permission_required = 'program.change_program'

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
@login_required
@permission_required('program.delete_program', raise_exception=True)
def delete_program(request, department_pk, pk, *args, **kwargs):
    if request.method == "POST":
        program = get_object_or_404(Program, pk=pk)
        program.delete()
        return redirect(
            reverse('myadmin:department',
                    kwargs={"pk": department_pk}) + '?deleted_program=1')
    return redirect(reverse('myadmin:department', kwargs={'pk': pk}))


# List Courses
class CourseListView(LoginRequiredMixin, PermissionRequiredMixin, generic_views.ListView):
    queryset = Course.objects.all()
    template_name = 'organization/course_list.html'
    context_object_name = 'courses'
    permission_required = 'course.view_course'

    def get_context_data(self, **kwargs):
        message = None
        if self.request.GET.get('course_added') == '1':
            message = 'Course added successfully!'
        kwargs['message'] = message
        return super().get_context_data(**kwargs)


# add course
class AddCourseView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    model = Course
    form_class = CourseForm
    template_name = 'organization/course_add.html'
    permission_required = 'course.add_course'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        course_form = self.form_class()

        return render(request, self.template_name, context={
            'course_form': course_form,
        })

    def post(self, request, *args, **kwargs):
        course_form = self.form_class(request.POST)
        if course_form.is_valid():
            course = course_form.save(commit=False)
            course.created_by = request.user
            course.save()
            return redirect(reverse('myadmin:course_list') + "?course_added=1")
        return render(request, self.template_name, context={
            'course_form': course_form,
        })


# View Course
class CourseDetailView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    template_name = 'organization/course.html'
    model = Course
    permission_required = 'course.view_course'
    raise_exception = True

    def get(self, request, pk, *args, **kwargs):
        course = get_object_or_404(self.model, pk=pk)
        classrooms = Classroom.objects.filter(course=course)
        return render(request, self.template_name, context={
                        'course': course, 'classrooms': classrooms
                        })


# Edit Courses
class EditCourseView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    template_name = 'organization/course_edit.html'
    form_class = CourseForm
    model = Course
    permission_required = 'course.change_course'
    raise_exception = True

    def get(self, request, pk, *args, **kwargs):
        course = get_object_or_404(self.model, pk=pk)
        course_form = self.form_class(instance=course)
        return render(request, self.template_name,
                      {"course_form": course_form})

    def post(self, request, pk, *args, **kwargs):
        course = get_object_or_404(self.model, pk=pk)
        course_form = self.form_class(data=request.POST, instance=course)
        if course_form.is_valid():
            course_form.save()
            return redirect(reverse('myadmin:course', kwargs={
                "pk": pk
            }))
        return render(request, self.template_name,
                      {"course_form": course_form})


# Delete Course
@login_required
@permission_required('course.delete_course', raise_exception=True)
def delete_course(request, pk, *args, **kwargs):
    if request.method == "POST":
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return redirect(
            reverse('myadmin:course_list') + '?deleted_program=1')
    return redirect(reverse('myadmin:course_list'))


class AddUserToProgramView(LoginRequiredMixin, PermissionRequiredMixin,
                           views.View):
    template_name = 'organization/program_add_user.html'
    form_class = AddUsersToProgramForm
    permission_required = 'program.change_program'
    raise_exception = True

    def get(self, request, department_pk, pk, *args, **kwargs):
        program = get_object_or_404(Program, pk=pk, department=department_pk)
        add_user_program_form = self.form_class(
            initial={
                'program': program
            }
        )
        return render(request, self.template_name, {
            'add_user_program_form': add_user_program_form
        })

    def post(self, request, department_pk, pk, *args, **kwargs):
        program = get_object_or_404(Program, pk=pk, department=department_pk)
        add_user_program_form = self.form_class(
            initial={
                'program': program
            }, data=request.POST
        )
        message = ''
        if add_user_program_form.is_valid():
            program = add_user_program_form.cleaned_data['program']
            emails = add_user_program_form.cleaned_data['emails']
            failed_emails = []
            success_emails = []

            for email in emails:
                try:
                    user = User.objects.get(email=email)
                    if user.user_type == User.UserType.student:
                        user.student.faculty = program
                        success_emails.append(email)

                except User.DoesNotExist:
                    failed_emails.append(email)
                    continue

            if success_emails:
                message = f'{", ".join(success_emails)} added to {program}.'

            if failed_emails:
                message += f' {", ".join(failed_emails)} users not found.'

        return render(request, self.template_name, {
            'add_user_program_form': add_user_program_form,
            'message': message
        })
