from django import forms
from django.contrib.auth import get_user_model
from .models import Address, Student, Teacher, User

USER = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "email",
        "placeholder": "eg. johndoe@myemail.com"
    }))
    password = forms.CharField(widget=forms.PasswordInput())


"""
    The SignUpFormOne & SignUpFormTwo is a ModelForm that has the fields as below which will be rendered 
    into the template named signup.html. 
    The Purpose of using two ModelForms for the same Model is that the two model forms will be rendered
    in sequence one after another such that the user won't be intimidated seeing large number of form fields in 
    a single page.
"""

class SignUpFormOne(forms.ModelForm):
    class Meta:
        model   = User
        fields  = ['email', 'password', 'first_name', 'last_name', 'username']
    

class SignUpFormTwo(forms.ModelForm):
    class Meta:
        model = User
        fields = [ 'phone_num', 'date_of_birth', 'blood_group', 'citizenship_num']



class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_num', 'date_of_birth',
                    'blood_group', 'citizenship_num', 'add_email', 'add_phone_num'
        ]


class TeacherInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['designation', 'year_joined', 'classrooms', 'departments']


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_number', 'classrooms', 'faculty', 'department']


class InviteForm(forms.Form):
    email = forms.EmailField(label='Join Email')