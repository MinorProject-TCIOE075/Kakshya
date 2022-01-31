from django.db import models
from django.utils import timezone

class Department(models.Model):
    dep_name        = models.CharField(max_length=250, unique=True, verbose_name="Department Name")
    created_on      = models.DateField(null=True, blank=True)
    modified_on     = models.DateField(null=True, blank=True, default=timezone.now)
    dep_code        = models.CharField(max_length=5, null=True, blank=True, unique=True, verbose_name="Department Code")

    def __str__(self):
        return f'{self.dep_name}'


class Program(models.Model):
    department      = models.ForeignKey(Department, on_delete=models.CASCADE)
    pr_code         = models.CharField(max_length=4, unique=True, verbose_name="Program Code")
    pr_name         = models.CharField(max_length=250, null=True, blank=True, verbose_name="Program")
    created_on      = models.DateTimeField(null=True, blank=True)
    modified_on     = models.DateTimeField(null=True, blank=True, default=timezone.now)    
    year            = models.IntegerField(default=1, null=True, blank=True)  


    def __str__(self):
        return f'{self.pr_code}'
