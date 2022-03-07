from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from .managers import UserManager


# Create your models here.
class User(AbstractUser):
    class UserType(models.TextChoices):
        student = "Student"
        teacher = 'Teacher'

    class UserRoles(models.TextChoices):
        staff = "Staff"
        super_admin = 'SuperAdmin'

    email = models.EmailField(_('email address'), unique=True, null=True,
                              blank=True)
    user_type = models.CharField(max_length=20, choices=UserType.choices)
    phone_num = models.CharField(max_length=14, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True,
                                     verbose_name="Date of Birth")
    blood_group = models.CharField(max_length=4, blank=True, null=True,
                                   verbose_name="Blood Group")
    citizenship_num = models.CharField(max_length=20, unique=True, null=True,
                                       blank=True,
                                       verbose_name="Citizenship Number")
    add_email = models.EmailField(_("Additional Email"), blank=True, null=True)
    add_phone_num = models.CharField(max_length=14, null=True, blank=True)

    """
        To query teachers only use => User.users.teachers()
        Syntax: <model_name>.<manager_name>.<manager_method>

        To query students only use => User.users.students()
        To query all users use User.objects.all() or User.users.all()
    """
    users = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]

    class Meta:
        permissions = [
            ('post_notice', "can post notices about classes"),
            ("assign_assignments", "can assign assignments to students")
        ]

    def get_absolute_url(self):
        return reverse("auth:user_detail", kwargs={'pk': self.pk})


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='student')
    year_joined = models.DateField(auto_now=False, auto_now_add=False,
                                   null=True, blank=True)
    roll_number = models.CharField(max_length=12, unique=True, null=True,
                                   blank=True)
    classrooms = models.IntegerField(null=True, blank=True)
    faculty = models.ForeignKey('organization.Program', on_delete=models.CASCADE, null=True)
    department = models.ForeignKey('organization.Department', on_delete=models.CASCADE,
                                   null=True)

    def __str__(self):
        return f'{self.user.username}'

    @property  # the property decorator here is used to access the method withoud parentheses ie. like obj.enrolledYear not obj.enrolledYear()
    def enrolledYear(self):
        return self.year_joined.strftime("%Y")


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='teacher')
    designation = models.CharField(null=True, blank=True, max_length=100)
    year_joined = models.DateField(auto_now_add=False, auto_now=False,
                                   null=True, blank=True)
    classrooms = models.IntegerField(null=True, blank=True)
    departments = models.ForeignKey('organization.Department', on_delete=models.CASCADE,
                                    null=True)

    def __str__(self):
        return f'{self.user.username}'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_permanent = models.BooleanField(default=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} {self.address}"
