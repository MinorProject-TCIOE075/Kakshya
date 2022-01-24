from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


# Create your models here.
class Department(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=4)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.code


class Program(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=4)
    year = models.CharField(max_length=4)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_by = models.ForeignKey(USER, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.code}-{self.year} -- {self.department}'


class Course(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=6)
    created_by = models.ForeignKey(USER, related_name='creator', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}-{self.code}'
