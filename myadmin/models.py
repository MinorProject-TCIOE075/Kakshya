import smtplib
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import models
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, smart_str


from authentication.models import User


class Invitation(models.Model):
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=User.UserType.choices)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def send_invitation(self, request, *args, **kwargs):
        current_site = get_current_site(request=request).domain
        relative_link = reverse(
            'auth:signup'
        )

        encoded_invitation_id = urlsafe_base64_encode(smart_bytes(self.email))

        abs_url = 'http://' + current_site + relative_link + encoded_invitation_id

        email_body = render_to_string(
            'myadmin/invitation_email.html', {
                'abs_url': abs_url
            })
        data = {
            'email_body': email_body,
            'to_email': self.email,
            'email_subject': 'You are Invited!!'
        }

        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.content_subtype = 'html'
        try:
            email.send(fail_silently=False)
        except smtplib.SMTPException:
            return False
        return True

    def __str__(self):
        return self.email
