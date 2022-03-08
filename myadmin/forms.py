from django import forms
from django.contrib.auth.models import Permission
from django.core.validators import EmailValidator, ValidationError

from authentication.models import User


class InvitationForm(forms.Form):
    emails = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}),
                             help_text="Enter emails seperated by commas.")
    user_type = forms.ChoiceField(choices=User.UserType.choices)

    def clean_emails(self):
        emails = self.cleaned_data['emails']
        invalid_emails = []

        emails = [email.strip() for email in emails.split(',')]

        for email in emails:
            try:
                validate = EmailValidator()
                validate(email)
            except ValidationError:
                invalid_emails.append(email)

        if invalid_emails:
            raise ValidationError(
                f'Emails "%(emails)s" are invalid.',
                code='invalid',
                params={
                    'emails': ", ".join(invalid_emails)
                }
            )

        return list(set(emails))


class UserEditFormMyadmin(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['password', 'groups', 'user_permissions']


class UserPermissionsForm(forms.ModelForm):
    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = User
        fields = ['user_permissions', ]
