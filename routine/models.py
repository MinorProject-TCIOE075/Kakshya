from django.contrib.auth import get_user_model
from django.db import models

from organization.models import Program, Course

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
    program = models.ForeignKey(Program, related_name='daily_routines', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.day} - {self.program}'


class RoutineCourse(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject_teacher = models.ForeignKey(USER, on_delete=models.SET_NULL,
                                        null=True)
    is_cancelled = models.BooleanField(default=False, null=True, blank=True)
    daily_routine = models.ForeignKey(DailyRoutine, related_name='courses',
                                      on_delete=models.CASCADE)
    cancelled_by = models.ForeignKey(USER, related_name='cancelled_courses',
                                     on_delete=models.SET_NULL, null=True,
                                     blank=True)

    def __str__(self):
        return f'{self.course} - {self.daily_routine}'
