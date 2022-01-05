from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login

from .forms import LoginForm

# Create your views here.


class LoginView(View):
    template_name = "login-page.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        login_form = LoginForm()
        return render(request, self.template_name, context={'login_form': login_form})

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            print(login_form.cleaned_data)
            email = login_form.cleaned_data.get("username", None)
            password = login_form.cleaned_data.get("password", None)

            user = authenticate(username=email, password=password)
            if user:
                login(request, user)

            print("credentials_invalid", user)

        return render(request, self.template_name, context={'login_form': login_form})
