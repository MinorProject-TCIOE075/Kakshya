from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "email",
        "placeholder": "eg. johndoe@myemail.com"
    }))
    password = forms.CharField(widget=forms.PasswordInput())
