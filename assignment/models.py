from email.policy import default
from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils import timezone
from organization.models import Course

User = settings.AUTH_USER_MODEL


class Assignment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateTimeField()
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=250)
    file = models.FileField(upload_to='assignments/')
    close_date = models.DateTimeField()
    points = models.IntegerField()
    created_on = models.DateTimeField(auto_now=True)
    modified_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Assignment for {self.title}"

    def get_absolute_url(self):
        return reverse('assignment:assignment_detail', kwargs = {'pk': self.pk})


class AssignmentSubmission(models.Model):
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='submitted')
    grade = models.IntegerField(default=0)
    file = models.FileField(upload_to='submission/')
    created_on = models.DateTimeField(auto_now=True)
    modified_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.submitted_by.username} on {self.created_on}"

    def get_absolute_url(self):
        return reverse('assignment:submission_detail', kwargs = {'pk': self.pk})