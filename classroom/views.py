import uuid

from django import views
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy
from django.views import generic as generic_views
from assignment.models import Assignment

from organization.models import Program
from .forms import CommentForm, CreateClassroomForm, CreatePostForm, EditPostForm
from .models import Classroom, Post


class ClassroomList(generic_views.ListView):
    template_name = 'classroom/classroom_list.html'
    context_object_name = 'classrooms'
    model = Classroom


class CreateClassroomView(views.View):
    template_name = 'classroom/classroom_add.html'
    model = Classroom
    form_class = CreateClassroomForm

    def get(self, request, department_pk, program_pk, *args, **kwargs):
        program = get_object_or_404(Program, pk=program_pk,
                                    department=department_pk)
        create_classroom_form = self.form_class()
        return render(request, self.template_name,
                      {
                          'classroom_form': create_classroom_form,
                          'program': program
                      })

    def post(self, request, department_pk, program_pk, *args, **kwargs):
        program = get_object_or_404(Program, pk=program_pk,
                                    department=department_pk)
        create_classroom_form = self.form_class(request.POST)
        if create_classroom_form.is_valid():
            classroom = create_classroom_form.save(commit=False)
            members = create_classroom_form.cleaned_data.get('member', None)
            classroom.program = program
            classroom.created_by = request.user
            classroom.member.add(members.id)
            classroom.save()

        return render(request, self.template_name,
                      {
                          'classroom_form': create_classroom_form,
                          'program': program
                      })


class EditClassroomView(views.View):
    template_name = 'classroom/classroom_edit.html'
    model = Classroom
    form_class = CreateClassroomForm

    def get(self, request, department_pk, program_pk, pk, *args, **kwargs):
        program = get_object_or_404(Program, pk=program_pk,
                                    department=department_pk)

        classroom = get_object_or_404(Classroom, pk=pk)

        create_classroom_form = self.form_class(instance=classroom)
        return render(request, self.template_name,
                      {
                          'classroom_form': create_classroom_form,
                          'program': program
                      })

    def post(self, request, department_pk, program_pk, pk, *args, **kwargs):
        program = get_object_or_404(Program, pk=program_pk,
                                    department=department_pk)
        classroom = get_object_or_404(Classroom, pk=pk)

        create_classroom_form = self.form_class(request.POST,
                                                instance=classroom)
        if create_classroom_form.is_valid():
            print(create_classroom_form.cleaned_data)
            create_classroom_form.save()
            return redirect(reverse('myadmin:program', kwargs={
                'department_pk': program.department.pk,
                'pk': program.pk
            }))

        return render(request, self.template_name,
                      {
                          'classroom_form': create_classroom_form,
                          'program': program
                      })


def archive_classroom(request, department_pk, program_pk, pk, *args, **kwargs):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        print("classroom archived")
        classroom.is_archived = True
        classroom.save()
        return redirect(reverse('myadmin:program', kwargs={
            'pk': classroom.program.pk,
            'department_pk': classroom.program.department.pk
        }) + '?archived=1')

    return redirect(reverse('myadmin:program', kwargs={
        'pk': classroom.program.pk,
        'department_pk': classroom.program.department.pk
    }))


def delete_classroom(request, department_pk, program_pk, pk, *args, **kwargs):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        print("classroom deleted")
        classroom.delete()
        return redirect(reverse('myadmin:program', kwargs={
            'pk': classroom.program.pk,
            'department_pk': classroom.program.department.pk
        }) + '?classroom_deleted=1')

    return redirect(reverse('myadmin:program', kwargs={
        'pk': classroom.program.pk,
        'department_pk': classroom.program.department.pk
    }))



class ClassroomDetailView(views.View):
    template_name = 'classroom/classroom_detail.html'
    model = Classroom

    def get(self, request, pk, *args, **kwargs):
        classroom = get_object_or_404(self.model, pk=pk)
        assignments = Assignment.objects.filter(classroom=classroom)
        posts = Post.objects.filter(classroom=classroom)
        print(classroom)
        context={
            'classroom': classroom,
            'assignments': assignments,
            'posts': posts
        }
        return render(request, self.template_name, context)




class PostList(generic_views.ListView):
    template_name = 'classroom/post_list.html'
    context_object_name = 'posts'
    model = Post


class CreatePostView(views.View):
    template_name = 'classroom/post_add.html'
    model = Post
    form_class = CreatePostForm

    def get(self, request, classroom_pk, *args, **kwargs):
        classroom = get_object_or_404(Classroom, pk=classroom_pk)
        create_post_form = self.form_class()
        return render(request, self.template_name,
                      {
                          'post_form': create_post_form,
                          'classroom': classroom
                      })

    def post(self, request, classroom_pk, *args, **kwargs):
        classroom = get_object_or_404(Classroom, pk=classroom_pk)
        create_post_form = self.form_class(request.POST, request.FILES)
        if create_post_form.is_valid():
            post = create_post_form.save(commit=False)
            post.classroom = classroom
            post.user = request.user
            post.save()
            return redirect(reverse_lazy("myadmin:classroom_detail", kwargs={
                                            'pk': classroom.pk
            }))

        return render(request, self.template_name,
                      {
                          'post_form': create_post_form,
                          'classroom': classroom
                      })



class PostDetail(views.View):
    template_name = 'classroom/post_detail.html'
    model = Post
    form_class = CommentForm

    def get(self, request, classroom_pk, post_pk, *args, **kwargs):
        post = get_object_or_404(self.model, classroom__pk=classroom_pk, pk=post_pk)
        comments = post.comment_set.filter(post=post)
        comment_form = self.form_class()
        context={
            'post': post,
            'comment_form': comment_form,
            'comments': comments
        }
        return render(request, self.template_name, context)

    def post(self, request, classroom_pk, post_pk, *args, **kwargs):
        post = get_object_or_404(self.model, classroom__pk=classroom_pk, pk=post_pk)
        comment_form = self.form_class(request.POST)
        comments = post.comment_set.filter(post=post)


        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.commented_by = request.user 
            comment.post = post 
            comment.save()
            return redirect(reverse_lazy("myadmin:post_detail", kwargs={
                                            'post_pk': post.pk,
                                            'classroom_pk': post.classroom.pk
            }))

        context = {
            'post': post,
            'comment_form': comment_form,
            'comments': comments
        }

        return render(request, self.template_name, context)


class EditPostView(views.View):
    model = Post
    form_class = EditPostForm
    template_name = 'classroom/post_edit.html'

    def get(self, request, classroom_pk, post_pk, *args, **kwargs):
        classroom = get_object_or_404(Classroom, id=classroom_pk)
        post = get_object_or_404(self.model, pk=post_pk)

        post_form = self.form_class(initial={
            'classroom': post.classroom,
           'caption': post.caption,
           'file': post.file,
        })
        return render(request, self.template_name, {
            "post_form": post_form,
            "classroom": classroom
        })

    def post(self, request, classroom_pk, post_pk, *args, **kwargs):
        classroom = get_object_or_404(Classroom, id=classroom_pk)
        post = get_object_or_404(self.model, pk=post_pk)

        post_form = self.form_class(request.POST, request.FILES)

        if post_form.is_valid():
            post.classroom = post_form.cleaned_data.get('classroom', 
                                                                    post.classroom)
            post.caption = post_form.cleaned_data.get('caption',
                                                               post.caption)
            post.file = post_form.cleaned_data.get('file', post.file)
            post.created_by = request.user
            post.save()
            return redirect(reverse_lazy('myadmin:post_detail', kwargs={
                                            'post_pk': post.pk,
                                            'classroom_pk': post.classroom.pk
            }))

        return render(request, self.template_name, {
            "post_form": post_form,
            'classroom': classroom
        })



def delete_post(request, classroom_pk, post_pk, *args, **kwargs):
    post = get_object_or_404(Post, classroom__pk=classroom_pk, pk=post_pk)
    if request.method == 'POST':
        print("classroom deleted")
        post.delete()            
        return redirect(reverse_lazy('myadmin:post_detail', kwargs={
                                            'post_pk': post.pk,
                                            'classroom_pk': post.classroom.pk
                                            }))

    return redirect(reverse('myadmin:classroom_detail', kwargs={
        'classroom_pk': post.classroom.pk,
    }))

