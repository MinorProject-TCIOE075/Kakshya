from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    class UserType(models.TextChoices):
        student = "Student"
        teacher = 'Teacher'

    class UserRoles(models.TextChoices):
        staff = "Staff"
        super_admin = 'SuperAdmin'

    email = models.EmailField(_('email address'), blank=True, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]
