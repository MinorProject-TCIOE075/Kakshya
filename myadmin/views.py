from django import views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin, PermissionDenied)
from django.shortcuts import render

from .forms import InvitationForm
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
