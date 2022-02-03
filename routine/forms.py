from django import forms
from django.core.exceptions import ValidationError

from .models import DailyRoutine, RoutineCourse


class DailyRoutineForm(forms.ModelForm):
    class Meta:
        model = DailyRoutine
        fields = "__all__"

    def clean(self):
        day = self.cleaned_data.get('day', None)
        program = self.cleaned_data.get('program', None)

        if not day or not program:
            raise ValidationError('All fields must be filled out properly.')

        if not self.instance.day:
            if DailyRoutine.objects.filter(day=day, program=program).exists():
                raise ValidationError('A routine for this day "%(day)s" and '
                                      'program"%(program)s" has already been '
                                      'created.', code='already_created',
                                      params={
                                          'day': day,
                                          'program': program
                                      })

        # Validate when used as an edit form
        if self.instance.day:
            if (self.instance.day != day) or (self.instance.program != program):
                if DailyRoutine.objects.filter(day=day,
                                               program=program).exists():
                    raise ValidationError(
                        'A routine for this day "%(day)s" and '
                        'program"%(program)s" has already exists.',
                        code='already_created',
                        params={
                            'day': day,
                            'program': program
                        })

        return super().clean()


class CourseForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'type': 'time'
    }))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'type': 'time'
    }))

    class Meta:
        model = RoutineCourse
        fields = ['daily_routine', 'course', 'subject_teacher', 'start_time',
                  'end_time', ]
