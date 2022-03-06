from django import forms
from .models import Classroom, Post


class CreateClassroomForm(forms.ModelForm):

    class Meta:
        model = Classroom
        fields = ['name', 'code', 'course']


class CreatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["file", 'caption']



class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["file", 'caption',]