from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from department.models import Department, Program


USER_ROLES = [
    ("T", _("Teacher")),
    ("S", _("Student")),
    ("St", _("Staff")),
    ("SU", _("SuperUser"))
]

# Create your models here.
class User(AbstractUser):
    class UserType(models.TextChoices):
        student = "Student"
        teacher = 'Teacher'

    class UserRoles(models.TextChoices):
        staff = "Staff"
        super_admin = 'SuperAdmin'

    email       = models.EmailField(_('email address'), blank=True, unique=True)
    user_role   = models.CharField(max_length=2, choices=USER_ROLES, default=None)

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



class Student(models.Model):
    user        =   models.ForeignKey(User, on_delete=models.CASCADE)
    year_joined =   models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    roll_number =   models.CharField(max_length=12, unique=True, null=True, blank=True)
    classrooms  =   models.IntegerField(null=True, blank=True)
    faculty     =   models.ForeignKey(Program, on_delete=models.CASCADE)
    department  =   models.ForeignKey(Department, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.username}'

    def enrolledYear(self):
        return self.year_joined.strftime("%Y")



class Teacher(models.Model):
    user        =   models.ForeignKey(User, on_delete=models.CASCADE)
    designation =   models.CharField(null=True, blank=True, max_length=100)
    year_joined =   models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    classrooms  =   models.IntegerField(null=True, blank=True)
    departments =   models.ForeignKey(Department, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.username}'