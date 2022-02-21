from django import forms
from django.core.exceptions import ValidationError

from authentication.models import Student


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

    additional_email = forms.EmailField(widget=forms.DateInput(attrs={
        'required': False
    }))
    additional_phone_number = forms.CharField(max_length=14,
                                              widget=forms.DateInput(attrs={
                                                  'required': False
                                              }))


class StudentProfileEditForm(ProfileEditForm):
    roll_number = forms.CharField(max_length=12)

    def clean_roll_number(self):
        roll_number = self.cleaned_data.get('roll_number')

        if Student.objects.filter(roll_number=roll_number).exists():
            raise ValidationError(
                "Roll number %(roll_number)s already exists. "
                "Please verify its yours.",
                code='invalid',
                params={
                    'roll_number': roll_number
                }
            )
        return roll_number


class TeacherProfileEditForm(ProfileEditForm):
    designation = forms.CharField(max_length=100)
