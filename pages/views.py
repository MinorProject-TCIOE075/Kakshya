from django import views
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

USER = get_user_model()


class ProfileView(views.View):
    template_name = 'pages/profile.html'

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(USER, username=username)
        return render(request, self.template_name, {'user': user})
