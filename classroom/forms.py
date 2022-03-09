from django import forms
from .models import Classroom, Post, Comment


class CreateClassroomForm(forms.ModelForm):

    class Meta:
        model = Classroom
        fields = ['name', 'code', 'course', 'member']


class CreatePostForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ["file", 'caption']



class EditPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["file", 'caption',]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["caption", ]