from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import user_passes_test
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .forms import *
from .tokens import account_activation_token

# from formtools.wizard.views import NamedUrlSessionWizardView


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


# # CUSTOM PASSWORD RESET VIEWS
# class CustomPasswordResetView(PasswordResetView):
#     email_template_name = 'authentication/password_reset_email.html'
#     template_name = 'authentication/password_reset_form.html'
#     success_url = reverse_lazy('auth:password_reset_done')

# class CustomPasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'authentication/password_reset_done.html'


# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'authentication/password_reset_confirm.html'


# class CustomPasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'authentication/password_reset_complete.html'    


# # SIGNUP FORM VIEW
# """
#     The FormWizardView is derived from the NamedUrlSessionWizardView which is a class of django-formtools
#     Django-formtools is a package that is used to render a django form in multiple steps.
#     The NamedUrlSessionWizard class stores the values of the fields into the session storage builtin in django
#     such that while a user submits a form and prompts to another step, the previously entered value should be stored
#     somewhere. Instead of using Sessions we can also use the browser based Cookies to store the values namely
#     NamedUrlCookiesWizardView.

#     form_list is a list of the form classes that the view function will render in multiple steps

#     the done() method is a method of NamedUrlSessionWizardView. The done() method is overridden in 
#     following class.
#     In simple terms, the done method is used to add our own logic as to what is to be done after the user 
#     submits the data.

#     all the validated data from the form_list is stored in the form_data variable as a dictionary.
#     After that an instance of the User model is created where all the cleaned data is passed as a dictionary.
#     After that save() method is called on the instance that saves the instance into the database. 
# """
# class FormWizardView(NamedUrlSessionWizardView):
#     template_name = 'authentication/signup.html'
#     form_list = [SignUpFormOne, SignUpFormTwo]


#     def done(self, form_list, **kwargs):
#         form_data = self.get_all_cleaned_data()
#         password = form_data.pop('password')
#         instance = User.objects.create(**form_data)
#         instance.set_password(password)
#         instance.save()
#         print(form_data)

#         return render(self.request, 'authentication/done.html', form_data)




# User views
class UserDetailView(DetailView):
    model = User
    template_name = 'authentication/user_detail.html'
    context_object_name = 'user'

def home(request):
   return render(request, 'authentication/home.html', context={})

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


@user_passes_test(lambda u: u.is_superuser)
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_active is set to false until the user activates it through the activation link
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            
            # Mail related configuration 
            subject = "Activation of Account"
            message = render_to_string(
                'authentication/acc_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    # creates an encoded uid from user's pk that is used in confirmation link
                    # when user clicks the link this uid is passed to the activate view and 
                    # is decoded there to determine which user is it
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    # creates the token to use in the email confirmation link for that particular user
                    'token': account_activation_token.make_token(user)
                }
            )
            to_email = form.cleaned_data.get('email') 
            email = EmailMessage(
                subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse(
                "An account activation link is send to your email address.Please check youe email"
            )
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        # the uid that is passed throught the confirmation link is decoded here
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    #  checks if the user is valid and token is actually valid fro the use
    if user is not None and account_activation_token.check_token(user,token):
        # if yes then the account is activated for the user and the user can log in now
        user.is_active = True
        user.save()
        login(request, user)
        print(user)
        return redirect("auth:home")
    else:
        return HttpResponse("The link is either expired or invalid")


