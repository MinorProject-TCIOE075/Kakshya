from django.db import models


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    member = models.ManyToManyField('authentication.User',
                                    related_name='members')
    course = models.ForeignKey('organization.Course', on_delete=models.CASCADE)
    program = models.ForeignKey('organization.Program',
                                on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)
