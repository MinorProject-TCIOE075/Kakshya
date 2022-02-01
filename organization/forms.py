from django import forms
from django.core.exceptions import ValidationError

from .models import Department, Program, Course


class DepartmentForm(forms.Form):
    name = forms.CharField(max_length=255)
    code = forms.CharField(max_length=4)

    def clean(self):
        name = self.cleaned_data.get('name', None)
        code = self.cleaned_data.get('code', None)

        if not name or not code:
            raise ValidationError("All fields must be filled properly.")

        if Department.objects.filter(code=code, name=name):
            raise ValidationError(
                f'Department with code "{code}" and name "{name}" already exists.')

        if Department.objects.filter(code=code):
            raise ValidationError(
                f'Department with code "{code}" already exists.')

        if Department.objects.filter(name=name):
            raise ValidationError(
                f'Department with code "{name}" already exists.')

        return super().clean()


class EditDepartmentForm(forms.Form):
    name = forms.CharField(max_length=255)
    code = forms.CharField(max_length=4)

    def clean(self):
        name = self.cleaned_data.get('name', None)
        code = self.cleaned_data.get('code', None)

        if not name or not code:
            raise ValidationError("All fields must be filled properly.")

        return super(EditDepartmentForm, self).clean()


class ProgramForm(forms.Form):
    name = forms.CharField(max_length=255)
    code = forms.CharField(max_length=4)
    year = forms.CharField(max_length=4)
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    def clean(self):
        name = self.cleaned_data.get('name', None)
        code = self.cleaned_data.get('code', None)
        year = self.cleaned_data.get('year', None)
        department = self.cleaned_data.get('department', None)

        if not name or not code or not year or not department:
            raise ValidationError("All fields must be provided.")
        if Program.objects.filter(name=name, code=code, year=year, department=department):
            raise ValidationError(f'A program with code {code}-{year} already exists.')
        return super().clean()

    def clean_year(self):
        year = self.cleaned_data.get('year', None)
        # Validate if a valid year is given
        if not year.isnumeric() and not len(year) == 4:
            raise ValidationError("Please enter a valid year.")
        return year


class EditProgramForm(forms.Form):
    name = forms.CharField(max_length=255)
    code = forms.CharField(max_length=4)
    year = forms.CharField(max_length=4)
    department = forms.ModelChoiceField(queryset=Department.objects.all())

    def clean(self):
        name = self.cleaned_data.get('name', None)
        code = self.cleaned_data.get('code', None)
        year = self.cleaned_data.get('year', None)
        department = self.cleaned_data.get('department', None)

        if not name or not code or not year or not department:
            raise ValidationError("All fields must be provided.")
        return super().clean()

    def clean_year(self):
        year = self.cleaned_data.get('year', None)
        # Validate if a valid year is given
        if not year.isnumeric() and not len(year) == 4:
            raise ValidationError("Please enter a valid year.")
        return year


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code']

    def clean_code(self):
        code = self.cleaned_data.get('code', None)
        if not code:
            raise ValidationError('Code not provided')

        if Course.objects.filter(code=code).exists():
            raise ValidationError(f'Course with code "{code}" is already added.')
        return code
