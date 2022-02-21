from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView,
    PasswordResetCompleteView
)
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import View, DetailView
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode

from .forms import *
from myadmin.models import Invitation


class LoginView(View):
    template_name = "authentication/login-page.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print("hello", request.user.username)
            return redirect("/")
        message = None

        signup_success = request.GET.get('signup_success', None)
        already_registered = request.GET.get('already_registered', None)
        not_invited = request.GET.get('not_invited', None)
        if not_invited:
            message = 'Sorry. You\'re not invited to KAKSHYA. Contact admins.'
        if already_registered:
            message = 'Already registered. Please login.'
        if signup_success == '1':
            message = 'SignUp successful. Please login.'
        elif signup_success == '0':
            message = 'SignUp failed please follow the link in your email.'
        login_form = LoginForm()
        return render(request, self.template_name,
                      context={'login_form': login_form, 'message': message})

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

        return render(request, self.template_name,
                      context={'login_form': login_form})


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


class SignUpView(View):
    template_name = 'authentication/signup.html'
    form_class = SignUpForm

    def get(self, request, invitation_token, *args, **kwargs):
        try:
            invitation_email = smart_str(
                urlsafe_base64_decode(invitation_token))
        except DjangoUnicodeDecodeError:
            print("Invalid token!")
            return redirect(reverse('auth:login'))
        # print(invitation_email)
        if User.objects.filter(email=invitation_email).exists():
            return redirect(reverse('auth:login') + '?already_registered=1')
        invitation = None
        try:
            invitation = Invitation.objects.get(email=invitation_email)
        except Invitation.DoesNotExist:
            print("Does Not exist")
            return redirect(reverse('auth:login') + '?not_invited=1')

        if request.user.is_authenticated:
            logout(request)

        signup_form = self.form_class(initial={
            'email': invitation.email,
            'user_type': invitation.user_type,
        })
        return render(request, self.template_name, {
            'signup_form': signup_form
        })

    def post(self, request, invitation_token, *args, **kwargs):
        signup_form = self.form_class(request.POST)
        try:
            invitation_email = smart_str(
                urlsafe_base64_decode(invitation_token))
        except DjangoUnicodeDecodeError:
            print("Invalid token!")
            return redirect(reverse('auth:login'))
        # print(invitation_email)
        if User.objects.filter(email=invitation_email).exists():
            return redirect(reverse('auth:login') + '?already_registered=1')
        try:
            invitation = Invitation.objects.get(email=invitation_email)
        except Invitation.DoesNotExist:
            print("Does Not exist")
            return redirect(reverse('auth:login') + '?not_invited=1')
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.set_password(signup_form.cleaned_data.get('password'))
            user.user_type = invitation.user_type
            user.save()

            if user.user_type == USER.UserType.student:
                student = Student()
                student.user = user
                student.save()

            if user.user_type == USER.UserType.teacher:
                teacher = Teacher()
                teacher.user = user
                teacher.save()

            return redirect(reverse('auth:login') + '?signup_success=1')
        return render(request, self.template_name, {
            'signup_form': signup_form
        })


# User views
class UserDetailView(DetailView):
    model = USER
    template_name = 'authentication/user_detail.html'
    context_object_name = 'user'


def home(request):
    return render(request, 'authentication/home.html', context={})


#  Teacher Update Info
@login_required
def UpdateTeacherProfile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST or None, instance=request.user)

        profile_form = TeacherInfoUpdateForm(request.POST,
                                             instance=request.user.teacher)

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

#
# # INVITATION VIEW
# def invite(request):
#     if request.method == "POST":
#         form = InviteForm(request.POST)
#         if form.is_valid():
#             invitation = Invitation.objects.create(
#                 email=form.cleaned_data['email'],
#                 # this token is a randomly generated 20 characters alpanumeric token
#                 # this token will be used to check if the link is invitation link is valid
#                 token=User.objects.make_random_password(20),
#                 sender=request.user
#             )
#             invitation.save()
#             invitation.send()
#             return HttpResponse(
#                 '<p>An invitation link is sent to your email.Please check you email.</p>')
#
#     else:
#         form = InviteForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'authentication/invite.html', context)


# def accept_invitation(request, token):
#     invitation = get_object_or_404(Invitation, token__exact=token)
#     request.session['invitation'] = invitation.id
#     return HttpResponseRedirect("auth:signup")
