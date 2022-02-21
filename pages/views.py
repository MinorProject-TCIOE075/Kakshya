from django import views
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from .forms import TeacherProfileEditForm, StudentProfileEditForm

USER = get_user_model()


class ProfileView(views.View):
    template_name = 'pages/profile.html'

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(USER, username=username)
        return render(request, self.template_name, {'user': user})


class ProfileEdit(views.View):
    template_name = 'pages/profile_edit.html'
    form_class = StudentProfileEditForm

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(USER, username=username)

        profile_edit_form = StudentProfileEditForm()

        return render(request, self.template_name, {'profile_edit_form': profile_edit_form})
