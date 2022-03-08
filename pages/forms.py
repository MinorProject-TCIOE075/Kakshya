from django import forms
from django.core.exceptions import ValidationError

from authentication.models import Student
from organization.models import Program


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone_number = forms.CharField(max_length=14)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date'
    }))
    blood_group = forms.CharField(max_length=4)
    citizenship_number = forms.CharField(max_length=20)
    year_joined = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date'
    }))

    # additional_email = forms.EmailField(widget=forms.EmailInput(attrs={
    #     'required': False
    # }))
    # additional_phone_number = forms.CharField(max_length=14,
    #                                           widget=forms.TextInput(attrs={
    #                                               'required': False
    #                                           }))


class StudentProfileEditForm(ProfileEditForm):
    roll_number = forms.CharField(max_length=12)
    program = forms.ModelChoiceField(queryset=Program.objects.all())


class TeacherProfileEditForm(ProfileEditForm):
    designation = forms.CharField(max_length=100)
