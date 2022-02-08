from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Assignment, AssignmentSubmission


class AssignmentForm(forms.ModelForm):
    
    class Meta:
        model = Assignment
        fields = ('course', 'title', 'due_date', 'details', 'file', 'close_date', 'points')
        widgets = {
        'due_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select due date', 'type':'date'}),
        'close_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select closing date', 'type':'date'}),
        }

    def clean(self):
        title = self.cleaned_data.get('title', None)
        details = self.cleaned_data.get('details', None)
        due_date = self.cleaned_data.get('due_date', None)
        close_date = self.cleaned_data.get('close_date', None)
        points = self.cleaned_data.get('points', None)
        file = self.cleaned_data.get('file', None)

        msg = ""
        if not title or not details or not file:
            raise ValidationError("Title and details must be filled")
        
        if not points or not isinstance(points, int):
            raise ValidationError("Points is not set or is not an integer")
           

        if not due_date or not close_date:
            msg = "Due date or close date not specified"
            self.add_error("NoneType", msg)

        elif due_date < timezone.now() or close_date < timezone.now():
            msg = "Invalid date selected"
            self.add_error("due_date", msg)

        elif due_date > close_date:
            msg = "Due date is beyond closing date"
            self.add_error("close_date", msg)
        
        else:
            print("all good")
        return super(AssignmentForm, self).clean()


class EditAssignmentForm(forms.Form):
    title = forms.CharField(max_length=100)
    details = forms.CharField(max_length=250, widget=forms.Textarea())
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(format=('%m/%d/%Y'), attrs={'type': 'date'}))
    close_date = forms.DateTimeField(widget=forms.DateTimeInput(format=('%m/%d/%Y'), attrs={'type': 'date'}))
    points = forms.IntegerField(widget=forms.TextInput())
    file = forms.FileField()

    def clean(self):
        title = self.cleaned_data.get('title', None)
        details = self.cleaned_data.get('details', None)
        due_date = self.cleaned_data.get('due_date', None)
        close_date = self.cleaned_data.get('close_date', None)
        points = self.cleaned_data.get('points', None)
        file = self.cleaned_data.get('file', None)

        msg = ""
        if not title or not details or not file:
            raise ValidationError("Title and details must be filled")
        
        if not points or not isinstance(points, int):
            raise ValidationError("Points is not set or is not an integer")
           

        if not due_date or not close_date:
            msg = "Due date or close date not specified"
            self.add_error("NoneType", msg)

        elif due_date < timezone.now() or close_date < timezone.now():
            msg = "Invalid date selected"
            self.add_error("due_date", msg)

        elif due_date > close_date:
            msg = "Due date is beyond closing date"
            self.add_error("close_date", msg)
        
        else:
            print("all good")
        return super(EditAssignmentForm, self).clean()


class AssignmentSubmitForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file',]

    def clean_file(self):
        file = self.cleaned_data.get('file', None)
        if not file:
            raise ValidationError('File is not selected')
        
        return file


class AssignmentReturnForm(forms.Form):
    grade = forms.IntegerField(widget=forms.NumberInput())

    def clean_grade(self):
        grade = self.cleaned_data.get('grade', None)
        if not grade:
            raise ValidationError("You should assign the grade")
        return grade