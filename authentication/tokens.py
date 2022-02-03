from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
# six is a python module that is used as a utility to convert a particular text into unicode format


"""
    PasswordResetTokenGenerator is a django class to create a unique token for password reset.
    The _make_hash_value() method is overridden in the TokenGenerator class below which uses
    the user id, timestamp and the is_active boolean to create a unique token for creating a
    new use object. 
"""

class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()