import uuid
from django.db import models


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    member = models.ManyToManyField('authentication.User',
                                    related_name='members')
    course = models.ForeignKey('organization.Course', on_delete=models.CASCADE)
    program = models.ForeignKey('organization.Program',
                                on_delete=models.CASCADE)
    is_archived = models.BooleanField(default=False)
    created_by = models.ForeignKey('authentication.User',
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name} - {self.code}'


class Post(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    post_id = models.UUIDField(unique=True, default=uuid.uuid4())
    caption = models.TextField()
    file = models.FileField(upload_to='posts/files')
    classroom = models.ForeignKey('classroom.Classroom',
                                  on_delete=models.CASCADE)
    reacts = models.IntegerField(default=0, null=True, blank=True)
    reacted_by = models.ManyToManyField('authentication.User',
                                        related_name='post_reactors', blank=True)
    user = models.ForeignKey("authentication.User", on_delete=models.SET_NULL,
                             null=True)

    def __str__(self):
        return self.caption[:20]


class Comment(models.Model):
    comment_id = models.UUIDField(unique=True, default=uuid.uuid4())
    commented_by = models.ForeignKey("authentication.User", 
                                        on_delete=models.CASCADE, related_name="commentors")
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('classroom.Post', on_delete=models.CASCADE)
    caption = models.CharField(max_length=255)
    reacts = models.IntegerField(default=0, null=True, blank=True)
    reacted_by = models.ManyToManyField('authentication.User',
                                        related_name='comment_reactors')

    def __str__(self):
        return self.caption[:20]
