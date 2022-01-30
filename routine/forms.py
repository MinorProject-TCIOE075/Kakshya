from django import forms
from django.core.exceptions import ValidationError

from .models import DailyRoutine, RoutineCourse


class DailyRoutineForm(forms.ModelForm):
    class Meta:
        model = DailyRoutine
        fields = "__all__"

    def clean(self):
        print(self.cleaned_data)
        day = self.cleaned_data.get('day', None)
        program = self.cleaned_data.get('program', None)
        if not day or not program:
            raise ValidationError('All fields must be filled out properly.')

        if DailyRoutine.objects.filter(day=day, program=program).exists():
            raise ValidationError(f'A routine for this day "{day}" and '
                                  f'program"{program} has been already '
                                  f'created."')

        return super().clean()


class CourseForm(forms.ModelForm):
    class Meta:
        model = RoutineCourse
        fields = ['course', 'subject_teacher', 'start_time', 'end_time',
                  'daily_routine']
