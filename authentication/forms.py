from django import forms
from django.contrib.auth import get_user_model

from .models import Student, Teacher, User

USER = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "email",
        "placeholder": "eg. johndoe@myemail.com"
    }))
    password = forms.CharField(widget=forms.PasswordInput())


class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password',
                  'confirm_password', 'phone_num', 'date_of_birth',
                  'blood_group', 'citizenship_num', ]


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
