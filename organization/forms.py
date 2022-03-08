from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import Department, Course, Program
from classroom.models import Classroom


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
        if self.instance is None:
            if Course.objects.filter(code=code).exists():
                raise ValidationError(f'Course with code "{code}" is already added.')
        return code


class AddUsersToProgramForm(forms.Form):
    emails = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}),
                             help_text="Enter emails seperated by commas.")
    program = forms.ModelChoiceField(queryset=Program.objects.all())

    # noinspection DuplicatedCode
    def clean_emails(self):
        emails = self.cleaned_data['emails']
        invalid_emails = []

        emails = [email.strip() for email in emails.split(',')]

        for email in emails:
            try:
                validate = EmailValidator()
                validate(email)
            except ValidationError:
                invalid_emails.append(email)

        if invalid_emails:
            raise ValidationError(
                f'Emails "%(emails)s" are invalid.',
                code='invalid',
                params={
                    'emails': ", ".join(invalid_emails)
                }
            )

        return list(set(emails))


class AddTeacherToClassroomForm(forms.Form):
    emails = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}),
                             help_text="Enter emails seperated by commas.")
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all())

    # noinspection DuplicatedCode
    def clean_emails(self):
        emails = self.cleaned_data['emails']
        invalid_emails = []

        emails = [email.strip() for email in emails.split(',')]

        for email in emails:
            try:
                validate = EmailValidator()
                validate(email)
            except ValidationError:
                invalid_emails.append(email)

        if invalid_emails:
            raise ValidationError(
                f'Emails "%(emails)s" are invalid.',
                code='invalid',
                params={
                    'emails': ", ".join(invalid_emails)
                }
            )

        return list(set(emails))
