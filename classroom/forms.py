from django import forms
from .models import Classroom


class CreateClassroomForm(forms.ModelForm):

    class Meta:
        model = Classroom
        fields = ['name', 'code', 'course']
