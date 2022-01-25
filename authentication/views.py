from django.template import context
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.views import ( 
    PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView,
    PasswordResetCompleteView
)
from formtools.wizard.views import NamedUrlSessionWizardView


class LoginView(View):
    template_name = "authentication/login-page.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("hello", request.user.username)
            return redirect("/")
        login_form = LoginForm()
        return render(request, self.template_name, context={'login_form': login_form})

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            print(login_form.cleaned_data)
            email = login_form.cleaned_data.get("email", None)
            password = login_form.cleaned_data.get("password", None)

            user = authenticate(username=email, password=password)
            print(user)
            if user:
                login(request, user)
                print("logged in")
                return redirect("auth:home")
            print("credentials_invalid", user)

        return render(request, self.template_name, context={'login_form': login_form})


# USER LOGOUT VIEW
def user_logout(request):
    # USING DJANGO'S BUILT-IN LOGOUT FUNCTIONALITY from django.contrib.auth
    logout(request)
    return redirect('auth:home')
    # # REDIRECTING THE LOGGED OUT USER TO LOGIN PAGE  
    # return redirect("auth:login")


# CUSTOM PASSWORD RESET VIEWS
class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'authentication/password_reset_email.html'
    template_name = 'authentication/password_reset_form.html'
    success_url = reverse_lazy('auth:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'authentication/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'authentication/password_reset_complete.html'    


# SIGNUP FORM VIEW
"""
    The FormWizardView is derived from the NamedUrlSessionWizardView which is a class of django-formtools
    Django-formtools is a package that is used to render a django form in multiple steps.
    The NamedUrlSessionWizard class stores the values of the fields into the session storage builtin in django
    such that while a user submits a form and prompts to another step, the previously entered value should be stored
    somewhere. Instead of using Sessions we can also use the browser based Cookies to store the values namely
    NamedUrlCookiesWizardView.

    form_list is a list of the form classes that the view function will render in multiple steps

    the done() method is a method of NamedUrlSessionWizardView. The done() method is overridden in 
    following class.
    In simple terms, the done method is used to add our own logic as to what is to be done after the user 
    submits the data.

    all the validated data from the form_list is stored in the form_data variable as a dictionary.
    After that an instance of the User model is created where all the cleaned data is passed as a dictionary.
    After that save() method is called on the instance that saves the instance into the database. 
"""
class FormWizardView(NamedUrlSessionWizardView):
    template_name = 'authentication/signup.html'
    form_list = [SignUpFormOne, SignUpFormTwo]


    def done(self, form_list, **kwargs):
        form_data = self.get_all_cleaned_data()
        instance = User.objects.create(**form_data)
        instance.save()
        # print(form_list)
        # print("\n")
        print(form_data)

        return render(self.request, 'authentication/done.html', form_data)



def home(request):
    return HttpResponse(
        """<h1>Hello</h1>"""
        )

#  Teacher Update Info
@login_required
def UpdateTeacherProfile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST or None, instance=request.user)
        
        profile_form = TeacherInfoUpdateForm(request.POST, instance=request.user.teacher)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect("auth:home")
    else:
        user_form = UserUpdateForm()
        profile_form = TeacherInfoUpdateForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'authentication/update_teacher_info.html', context)


# @login_required
# def StudentProfileUpdate(request):
#     if request.method == "POST":
#         user_form = UserUpdateForm(request.POST or None, instance=request.user)
        
#         form = StudentUpdateForm(request.POST, instance=request.user.student)

#         if user_form.is_valid() and form.is_valid():
#             user = user_form.save(commit=False)
#             user.save()
#             form.save()

#             student = Student()
#             student.user = user

#             return redirect("auth:home")
#     else:
#         user_form = UserUpdateForm()
#         form = StudentUpdateForm()

#     context = {
#         'user_form': user_form,
#         'form': form
#     }

#     return render(request, 'authentication/student_update.html', context)


