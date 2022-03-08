from django import views
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin,
                                        PermissionDenied)
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse

from .decorators import staff_or_superuser_required
from .forms import InvitationForm, UserEditFormMyadmin, UserPermissionsForm
from .mixins import SuperuserOrStaffRequiredMixin
from .models import Invitation

USER = get_user_model()


# Create your views here.
class AdminDashboard(LoginRequiredMixin, views.View):
    template_name = 'myadmin/dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff or not request.user.is_superuser:
            raise PermissionDenied('Not a staff or superuser.')
        return render(request, self.template_name, {})


class InvitationView(LoginRequiredMixin, PermissionRequiredMixin, views.View):
    template_name = 'myadmin/invite_user.html'
    form_class = InvitationForm
    permission_required = 'invitation.create_invitation'
    raise_exception = True

    def get(self, request, *args, **kwargs):

        invitation_form = self.form_class()
        return render(request, self.template_name,
                      {'invitation_form': invitation_form})

    def post(self, request, *args, **kwargs):
        """
        When the request is posted, the emails are returned from the form after
        validation. The exceptions handled by this method so far are:
        - Many invitations in one go
        - No duplicate invitations
        - If already invited, just send the email again
        - If user already exists, Nothing happens i.e. No invitation, no email.
        - If some emails are failed to send, the message is shown with a list
          of failed emails.
        """
        invitation_form = self.form_class(request.POST)
        if invitation_form.is_valid():
            user_type = invitation_form.cleaned_data.get('user_type')
            emails = invitation_form.cleaned_data.get('emails')
            failed_invitation_emails = []

            for email in emails:
                if not Invitation.objects.filter(email=email).exists():
                    invitation = Invitation()
                    invitation.email = email
                    invitation.user_type = user_type
                else:
                    invitation = Invitation.objects.get(email=email)

                if not USER.objects.filter(email=email).exists():
                    is_invited = invitation.send_invitation(request)
                    if is_invited:
                        invitation.save()
                    else:
                        failed_invitation_emails.append(email)

            print(failed_invitation_emails)
            if failed_invitation_emails:
                failed_emails = ', '.join(failed_invitation_emails)
                message = f"{failed_emails} were not invited. Please try again."
                return render(request, self.template_name,
                              {
                                  'invitation_form': self.form_class(initial={
                                      'emails': failed_emails,
                                      'message': message
                                  })
                              })
            else:
                message = 'Invitations Successful.'
            return render(request, self.template_name,
                          {
                              'invitation_form': self.form_class(),
                              'message': message
                          })

        return render(request, self.template_name,
                      {'invitation_form': invitation_form})


class UserListView(LoginRequiredMixin, SuperuserOrStaffRequiredMixin,
                   views.View):
    template_name = 'myadmin/user_list.html'

    def get(self, request, *args, **kwargs):
        users = USER.objects.all()
        message = ''
        deleted = request.GET.get('deleted', None)

        if deleted == '1':
            message = "User deleted successfully."
        paginated_users = Paginator(users, per_page=20)
        page_number = request.GET.get('page', 1)
        users = paginated_users.get_page(page_number)

        return render(request, self.template_name,
                      {'users': users, 'message': message})


class UserDetailView(LoginRequiredMixin, SuperuserOrStaffRequiredMixin,
                     views.View):
    template_name = 'myadmin/user.html'

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(USER, username=username)
        is_updated = request.GET.get('updated', None)
        message = ''
        if is_updated == '1':
            message = 'Updated Successfully'
        return render(request, self.template_name,
                      {'user': user, 'message': message})


class UserEditView(LoginRequiredMixin, SuperuserOrStaffRequiredMixin,
                   views.View):
    template_name = 'myadmin/user_edit.html'
    form_class = UserEditFormMyadmin

    def get(self, request, username, *args, **kwargs):
        user_edit_form = self.form_class(
            instance=get_object_or_404(USER, username=username))
        return render(request, self.template_name,
                      {'user_edit_form': user_edit_form})

    def post(self, request, username, *args, **kwargs):
        user_edit_form = self.form_class(
            instance=get_object_or_404(USER, username=username),
            data=request.POST)
        if user_edit_form.is_valid():
            user_edit_form.save()
            return redirect(
                reverse('myadmin:user_detail',
                        kwargs={'username': username}) + '?updated=1')
        return render(request, self.template_name,
                      {'user_edit_form': user_edit_form})


class UserPermissionUpdateView(LoginRequiredMixin,
                               SuperuserOrStaffRequiredMixin, views.View):
    template_name = 'myadmin/user_permissions.html'
    form_class = UserPermissionsForm

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(USER, username=username)
        update_permission_form = self.form_class(
            instance=user)
        return render(request, self.template_name,
                      {'update_permission_form': update_permission_form,
                       'user': user})

    def post(self, request, username, *args, **kwargs):
        user = get_object_or_404(USER, username=username)
        update_permission_form = self.form_class(
            instance=user, data=request.POST or None)
        if update_permission_form.is_valid():
            update_permission_form.save()
            return redirect(
                reverse('myadmin:user_detail',
                        kwargs={'username': username}) + '?updated=1')

        return render(request, self.template_name,
                      {'update_permission_form': update_permission_form,
                       'user': user})


@login_required
@staff_or_superuser_required
def delete_user(request, username, *args, **kwargs):
    if request.method == "POST":
        user = get_object_or_404(USER, username=username)
        user.is_active = False
        user.save()
        return redirect(reverse("myadmin:user_list") + "?deleted=1")
    return redirect(reverse("myadmin:user_list"))
