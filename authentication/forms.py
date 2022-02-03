from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Address, Student, Teacher, User

USER = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "email",
        "placeholder": "eg. johndoe@myemail.com"
    }))
    password = forms.CharField(widget=forms.PasswordInput())


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')



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