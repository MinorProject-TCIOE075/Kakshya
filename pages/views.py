from django import views
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.urls import reverse_lazy

from assignment.forms import (AssignmentSubmitForm,
                              AssignmentReturnForm, AssignmentForm
                              )
from assignment.models import Assignment, AssignmentSubmission
from authentication.models import Student, Teacher
from classroom.forms import CreatePostForm, CommentForm
from classroom.models import Classroom, Post
from routine.models import DailyRoutine, RoutineCourse
from .forms import StudentProfileEditForm, TeacherProfileEditForm

USER = get_user_model()


class ProfileView(LoginRequiredMixin, views.View):
    template_name = 'pages/profile.html'
    model = USER

    def get(self, request, username, *args, **kwargs):
        update_success = request.GET.get('update_success', None)
        message = None
        if update_success:
            message = "Update Successful."
        user = get_object_or_404(self.model, username=username)
        return render(request, self.template_name,
                      {'user': user, 'message': message})


class ProfileEdit(views.View):
    template_name = 'pages/profile_edit.html'

    def get(self, request, username, *args, **kwargs):
        if username is not request.user.username:
            return redirect(reverse('pages:profile', kwargs={
                'username': request.user.username,
            }))
        user = get_object_or_404(USER, username=username)
        if not user.user_type:
            user.user_type = USER.UserType.student
            user.save()
        if user.user_type == USER.UserType.student and \
                not Student.objects.filter(user=user).exists():
            student = Student()
            student.user = user
            student.save()

        if user.user_type == USER.UserType.teacher and \
                not Teacher.objects.filter(user=user).exists():
            teacher = Teacher()
            teacher.user = user
            teacher.save()

        profile_edit_form = None
        if user.user_type == USER.UserType.student:
            profile_edit_form = StudentProfileEditForm({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_num,
                'date_of_birth': user.date_of_birth,
                'blood_group': user.blood_group,
                'citizenship_number': user.citizenship_num,
                'year_joined': user.student.year_joined,
                'additional_email': user.add_email,
                'additional_phone_number': user.add_phone_num,
                'roll_number': user.student.roll_number,
                'faculty': user.student.faculty
            })

        if user.user_type == USER.UserType.teacher:
            profile_edit_form = TeacherProfileEditForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phone_num,
                'date_of_birth': user.date_of_birth,
                'blood_group': user.blood_group,
                'citizenship_number': user.citizenship_num,
                'year_joined': user.student.year_joined,
                'additional_email': user.add_email,
                'additional_phone_number': user.add_phone_num,
                'designation': user.student.roll_number,
            })

        return render(request, self.template_name,
                      {'profile_edit_form': profile_edit_form})

    def post(self, request, username, *args, **kwargs):
        user = get_object_or_404(USER, username=username)

        profile_edit_form = None

        if user.user_type == USER.UserType.teacher:
            profile_edit_form = TeacherProfileEditForm(request.POST)

        if user.user_type == USER.UserType.student:
            profile_edit_form = StudentProfileEditForm(request.POST)

        if profile_edit_form.is_valid():
            first_name = profile_edit_form.cleaned_data.get('username',
                                                            user.first_name)
            last_name = profile_edit_form.cleaned_data.get('last_name',
                                                           user.last_name)
            phone_number = profile_edit_form.cleaned_data.get('phone_number',
                                                              user.phone_num)
            date_of_birth = profile_edit_form.cleaned_data.get('date_of_birth',
                                                               user.date_of_birth)
            blood_group = profile_edit_form.cleaned_data.get('blood_group',
                                                             user.blood_group)
            citizenship_number = profile_edit_form.cleaned_data.get(
                'citizenship_number', user.citizenship_num)

            user.first_name = first_name
            user.last_name = last_name
            user.phone_num = phone_number
            user.date_of_birth = date_of_birth
            user.blood_group = blood_group
            user.citizenship_num = citizenship_number

            if user.user_type == USER.UserType.student:
                year_joined = profile_edit_form.cleaned_data.get('year_joined',
                                                                 user.student.year_joined)
                program = profile_edit_form.cleaned_data.get('program',
                                                             user.student.faculty)
                user.student.year_joined = year_joined
                user.student.faculty = program
                roll_number = profile_edit_form.cleaned_data.get(
                    'roll_number', user.student.roll_number)
                if roll_number != user.student.roll_number:
                    if Student.objects.filter(
                            roll_number=roll_number).exists():
                        profile_edit_form._errors['roll_number'] = (
                            u"The roll number already exists")
                        return render(request, self.template_name,
                                      {'profile_edit_form': profile_edit_form})
                user.student.roll_number = roll_number
                user.student.save()
                user.save()

            if user.user_type == USER.UserType.teacher:
                year_joined = profile_edit_form.cleaned_data.get('year_joined',
                                                                 user.teacher.year_joined)
                user.teacher.year_joined = year_joined
                user.teacher.designation = profile_edit_form.cleaned_data.get(
                    'designation', user.teacher.designation)
                user.teacher.save()
                user.save()

            return redirect(reverse('pages:profile', args=[user.username]))

        return render(request, self.template_name,
                      {'profile_edit_form': profile_edit_form})


class Dashboard(views.View):
    template_name = "pages/dashboard.html"

    def get(self, request, *args, **kwargs):
        print('here')
        user = request.user
        posts = []
        if user.user_type == USER.UserType.student:
            try:
                print('user')
                user_program = user.student.faculty.id
                classroom = Classroom.objects.filter(program=user_program)
                posts = Post.objects.filter(classroom__in=classroom.all())
            except Exception as e:
                print(e)
                user_program = None
                classroom = None
                posts = None

        if user.user_type == USER.UserType.teacher:
            classroom = Classroom.objects.filter(member=request.user)
            posts = Post.objects.filter(classroom__in=classroom.all())
        context = {
            'posts': posts
        }
        return render(request, self.template_name, context)


class ClassRoom(views.View):
    template_name = 'pages/classroom_list.html'
    model = Classroom

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == USER.UserType.student:
            try:
                classroom = Classroom.objects.filter(
                    program=user.student.faculty.id)
            except ValueError:
                classroom = None
            except AttributeError:
                classroom = None

        if user.user_type == USER.UserType.teacher:
            classroom = Classroom.objects.filter(member=request.user)
        context = {
            'classroom': classroom
        }
        return render(request, self.template_name, context)


class ClassRoomView(views.View):
    template_name = 'pages/classroom_detail.html'

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        pk = self.kwargs.get('pk')
        classroom = get_object_or_404(Classroom, id=pk)

        if user.user_type == USER.UserType.teacher:
            teacher = True
            assignments = Assignment.objects.filter(classroom=classroom,
                                                    created_by=user)
            posts = Post.objects.filter(classroom=classroom, user=user)

        elif user.user_type == USER.UserType.student:
            teacher = False
            assignments = Assignment.objects.filter(classroom=classroom)
            posts = Post.objects.filter(classroom=classroom)

        print(teacher)
        context = {
            'classroom': classroom,
            'assignments': assignments,
            'teacher': teacher,
            'posts': posts
        }
        return render(request, self.template_name, context)


class DailyRoutineView(views.View):
    template_name = 'pages/daily_routine.html'
    model = DailyRoutine

    def get(self, request, *args, **kwargs):
        user = request.user
        routines = None
        if user.user_type == USER.UserType.student:
            user = user.student
            if not user.faculty:
                return redirect(reverse('pages:not_associated_page'))
            routines = DailyRoutine.objects.filter(program=user.faculty.id)

        elif user.user_type == USER.UserType.teacher:
            routines = DailyRoutine.objects.all()

        context = {
            'routines': routines
        }
        return render(request, self.template_name, context)


class RoutineCourseView(views.View):
    template_name = 'pages/routine_course.html'
    model = RoutineCourse

    def get(self, request, pk, *args, **kwargs):
        daily_routine = get_object_or_404(DailyRoutine, id=pk)
        routine_course = RoutineCourse.objects.filter(
            daily_routine=daily_routine)

        user = request.user
        if user.user_type == USER.UserType.teacher:
            routine_course = RoutineCourse.objects.filter(
                subject_teacher=request.user)

        context = {
            'routine_course': routine_course
        }
        return render(request, self.template_name, context)


class StudentAssignment(views.View):
    template_name = 'pages/assignment_list.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == USER.UserType.student:
            if not user.student.faculty:
                return redirect(reverse('pages:not_associated_page'))
            user_program = user.student.faculty.id

            classroom = Classroom.objects.filter(program=user_program)
            assignments = Assignment.objects.filter(
                classroom__in=classroom.all())

        if user.user_type == USER.UserType.teacher:
            assignments = Assignment.objects.filter(created_by=user)
        context = {
            'assignments': assignments
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == USER.UserTyper.teacher:
            assignment_form = AssignmentForm(request.POST)
            if assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)


def assignment_detail(request, pk):
    template_name = 'pages/assignment_detail.html'
    user = request.user
    assignment = get_object_or_404(Assignment, id=pk)

    if user.user_type == USER.UserType.student:
        student = True
        user_program = user.student.faculty.id
        assignment_submit = assignment.assignmentsubmission_set.filter(
            assignment_id=assignment.id
        )
        new_submit = None
        if request.method == "POST":
            print("good")
            submit_form = AssignmentSubmitForm(request.POST, request.FILES)
            if submit_form.is_valid():
                new_submit = submit_form.save(commit=False)
                new_submit.assignment_id = assignment
                new_submit.submitted_by = user
                new_submit.save()
                return redirect('pages:student_assignment')

        else:
            submit_form = AssignmentSubmitForm()

        context = {
            'assignment': assignment,
            'assignment_submit': assignment_submit,
            'new_submit': new_submit,
            'submit_form': submit_form,
            'student': student
        }
    if user.user_type == USER.UserType.teacher:
        teacher = True
        assignment_submit = assignment.assignmentsubmission_set.filter(
            assignment_id=assignment.id
        )
        context = {
            'assignment': assignment,
            'teacher': teacher,
            'assignment_submit': assignment_submit
        }
    return render(request, template_name, context)


def submission_detail(request, pk):
    template_name = 'pages/submission_detail.html'
    submission = get_object_or_404(AssignmentSubmission, id=pk)
    user = request.user
    message = ""

    if user.user_type == USER.UserType.teacher:
        if submission.assignment_id.created_by == user:
            if request.method == "POST":
                return_form = AssignmentReturnForm(request.POST)
                if return_form.is_valid():
                    try:
                        submission.grade = return_form.cleaned_data.get(
                            'grade', submission.grade)
                        submission.status = "returned"
                        if submission.grade > submission.assignment_id.points:
                            message = "Grade cannot be greater than initial assignment points"

                        else:
                            submission.save()
                            return redirect("pages:dashboard")
                    except submission.grade > submission.assignment_id.points:
                        raise ValueError(
                            "Grade cannot be greater than assignment points")

            else:
                return_form = AssignmentReturnForm()

    context = {
        'submission': submission,
        'return_form': return_form,
        'message': message

    }

    return render(request, template_name, context)


class AddAssignmentView(views.View):
    template_name = 'pages/add_assignment.html'
    form_class = AssignmentForm

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        pk = self.kwargs.get('pk')
        classroom = get_object_or_404(Classroom, id=pk)
        assignments = Assignment.objects.filter(classroom=classroom)

        if user.user_type == USER.UserType.teacher:
            assignment_form = self.form_class()

        context = {
            'classroom': classroom,
            'assignments': assignments,
            'form': assignment_form
        }
        return render(request, self.template_name, context)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        classroom = get_object_or_404(Classroom, id=pk)
        assignments = Assignment.objects.filter(classroom=classroom)

        if user.user_type == USER.UserType.teacher:
            assignment_form = self.form_class(request.POST, request.FILES)
            if assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)
                assignment.classroom = classroom
                assignment.created_by = user
                assignment.course = classroom.course  # print(assignment)
                assignment.save()
                print(assignment)
                return redirect(reverse_lazy("pages:classroom_detail", kwargs={
                    'pk': classroom.pk
                }))
        context = {
            'form': assignment_form,
            'classroom': classroom,
            'assignments': assignments
        }

        return render(request, self.template_name, context)


class AddPostView(views.View):
    template_name = "pages/add_post.html"
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
            return redirect(reverse_lazy("pages:classroom_detail", kwargs={
                'pk': classroom.pk
            }))

        return render(request, self.template_name,
                      {
                          'post_form': create_post_form,
                          'classroom': classroom
                      })


class PostDetail(views.View):
    template_name = 'pages/post_detail.html'
    model = Post
    form_class = CommentForm

    def get(self, request, classroom_pk, post_pk, *args, **kwargs):
        post = get_object_or_404(self.model, classroom__pk=classroom_pk,
                                 pk=post_pk)
        comments = post.comment_set.filter(post=post)
        comment_form = self.form_class()
        context = {
            'post': post,
            'comment_form': comment_form,
            'comments': comments
        }
        return render(request, self.template_name, context)

    def post(self, request, classroom_pk, post_pk, *args, **kwargs):
        post = get_object_or_404(self.model, classroom__pk=classroom_pk,
                                 pk=post_pk)
        comment_form = self.form_class(request.POST)
        comments = post.comment_set.filter(post=post)

        if request.user.user_type == USER.UserType.teacher:
            teacher = True

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.commented_by = request.user
            comment.post = post
            comment.save()
            return redirect(reverse_lazy("pages:post_detail", kwargs={
                'post_pk': post.pk,
                'classroom_pk': post.classroom.pk
            }))

        context = {
            'post': post,
            'comment_form': comment_form,
            'comments': comments,
            'teacher': teacher
        }

        return render(request, self.template_name, context)


class SharedFiles(views.View):
    template_name = "pages/shared_files.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == USER.UserType.student:
            user_program = user.student.faculty.id
            classroom = Classroom.objects.filter(program=user_program)
            posts = Post.objects.filter(classroom__in=classroom.all())

        if user.user_type == USER.UserType.teacher:
            classroom = Classroom.objects.filter(member=user)
            posts = Post.objects.filter(classroom__in=classroom.all())

        return render(request, self.template_name, context={'posts': posts})


class NotAssociatedPage(LoginRequiredMixin, views.View):
    template_name = 'not_associated_page.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
