from django import views
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, render, get_object_or_404, redirect, reverse

from authentication.models import Student, Teacher
from .forms import StudentProfileEditForm, TeacherProfileEditForm
from classroom.models import Classroom
from assignment.models import Assignment
from routine.models import DailyRoutine, RoutineCourse
from assignment.forms import AssignmentSubmitForm, AssignmentReturnForm

USER = get_user_model()


class ProfileView(views.View):
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




def home(request):
    return HttpResponse("home")


class ClassRoom(views.View):
    template_name = 'pages/classroom_list.html'
    model = Classroom

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == USER.UserType.student:
            user = user.student
            classroom = Classroom.objects.filter(program=user.faculty.id)
        
        context = {
            'classroom': classroom
        }
        return render(request, self.template_name, context)


class DailyRoutineView(views.View):
    template_name = 'pages/daily_routine.html'
    model = DailyRoutine

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == USER.UserType.student:
            user = user.student
            routines = DailyRoutine.objects.filter(program=user.faculty.id)
        
        context = {
            'routines': routines
        }
        return render(request, self.template_name, context)


class RoutineCourseView(views.View):
    template_name = 'pages/routine_course.html'
    model = RoutineCourse

    def get(self, request, pk, *args, **kwargs):
        daily_routine = get_object_or_404(DailyRoutine, id=pk)
        routine_course = RoutineCourse.objects.filter(daily_routine=daily_routine)

        context = {
            'routine_course': routine_course
        }
        return render(request, self.template_name, context)


class StudentAssignment(views.View):
    template_name = 'pages/assignment_list.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == USER.UserType.student:
            user_program = user.student.faculty.id
            classroom = Classroom.objects.filter(program=user_program)
            assignments = Assignment.objects.filter(classroom__in=classroom.all())

            context = {
                'assignments': assignments
            }
        return render(request, self.template_name, context)


def assignment_detail(request, pk):
    template_name = 'pages/assignment_detail.html'
    user_program = request.user.student.faculty.id
    assignment = get_object_or_404(Assignment, id=pk)
    assignment_submit = assignment.assignmentsubmission_set.filter(assignment_id=assignment.id)
    new_submit = None   

    if request.method == "POST":
        submit_form = AssignmentSubmitForm(request.POST, request.FILES)
        if submit_form.is_valid():
            new_submit = submit_form.save(commit=False)
            new_submit.assignment_id = assignment
            new_submit.submitted_by = request.user
            new_submit.save()

    else:
        submit_form = AssignmentSubmitForm()
    
    context = {
        'assignment': assignment,
        'assignment_submit': assignment_submit,
        'new_submit': new_submit,
        'submit_form': submit_form
    }

    return render(request, template_name, context)





class ClassRoomView(views.View):
    template_name = 'pages/classroom_detail.html'

    def get(self, request, pk, *args, **kwargs):
        pk = self.kwargs.get('pk')
        classroom = get_object_or_404(Classroom, id=pk)
        assignments = Assignment.objects.filter(classroom=classroom)

        context = {
            'classroom': classroom,
            'assignments': assignments
        }
        return render(request, self.template_name, context)
