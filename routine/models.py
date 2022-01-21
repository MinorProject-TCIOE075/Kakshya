from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()


# Create your models here.
class DailyRoutine(models.Model):
    class DayChoices(models.TextChoices):
        SUNDAY = "SUN"
        MONDAY = "MON"
        TUESDAY = "TUE"
        WEDNESDAY = "WED"
        THURSDAY = "THU"
        FRIDAY = "FRI"
        SATURDAY = "SAT"

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    day = models.CharField(max_length=10, choices=DayChoices.choices)
    program = models.OneToOneField("Program", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.day} - {self.program}'


class Course(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject_teacher = models.OneToOneField(USER, on_delete=models.SET_NULL, null=True)
    is_cancelled = models.BooleanField(default=False, null=True, blank=True)
    daily_routine = models.ForeignKey(DailyRoutine, related_name='courses', on_delete=models.CASCADE)
    cancelled_by = models.OneToOneField(USER, related_name='cancelled_courses', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.daily_routine}'


class Program(models.Model):
    pass
