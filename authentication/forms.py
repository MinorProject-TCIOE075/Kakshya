from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Student, Teacher, User

USER = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "email",
        "placeholder": "eg. johndoe@myemail.com"
    }))
    password = forms.CharField(widget=forms.PasswordInput())


class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '*********'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': '*********'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'John'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Doe'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'cool_username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'mycoolemail123@example.com',
        'type': 'email'
    }))
    phone_num = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234567890'
    }))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date'
    }))
    blood_group = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'A+'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password',
                  'confirm_password', 'phone_num', 'date_of_birth',
                  'blood_group', 'citizenship_num', ]

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not password or not confirm_password:
            raise ValidationError("All fields not properly filled!")

        if password != confirm_password:
            raise ValidationError('Passwords do not match')

        return super().clean()


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = USER
        fields = ['username', 'first_name', 'last_name', 'phone_num',
                  'date_of_birth',
                  'blood_group', 'citizenship_num', 'add_email',
                  'add_phone_num'
                  ]


class TeacherInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['designation', 'year_joined', 'classrooms', 'departments']


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'classrooms', 'faculty', 'department']
