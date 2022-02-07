from django import forms
from django.core.exceptions import ValidationError

from .models import Assignment, AssignmentSubmission


class AssignmentForm(forms.ModelForm):
    
    class Meta:
        model = Assignment
        fields = ('course', 'title', 'due_date', 'details', 'file', 'close_date', 'points')
        widgets = {
        'due_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select due date', 'type':'date'}),
        'close_date': forms.DateInput(format=('%m/%d/%Y'), attrs={'class':'form-control', 'placeholder':'Select closing date', 'type':'date'}),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file', None)
        if not file:
            raise ValidationError('File is not selected')
        
        return file


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

        if not title or not details or not file:
            raise ValidationError("Title and details must be filled")
        
        if not due_date or not close_date:
            raise ValidationError("Due date and Closing date must be set properly")

        if due_date > close_date:
            raise ValidationError("Due date is beyond the closing date")
        
        return super(EditAssignmentForm, self).clean()

