from django import views
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .forms import (
    AssignmentForm, AssignmentReturnForm, 
    EditAssignmentForm, AssignmentSubmitForm
)
from .models import Assignment, AssignmentSubmission
from classroom.models import Classroom

class AssignmentList(generic.ListView):
    queryset = Assignment.objects.all()
    template_name = 'assignment/assignment_list.html'
    context_object_name = 'assignments'


class AddAssignmentView(LoginRequiredMixin, views.View):
    model = Assignment
    form_class = AssignmentForm
    template_name = 'assignment/assignment_add.html'


    def get(self, request, *args, **kwargs):
        assignment_form = self.form_class()
        context = {
            'assignment_form': assignment_form
        }

        return render(request, self.template_name, context)

    
    def post(self, request, *args, **kwargs):
        assignment_form = self.form_class(request.POST,  request.FILES)
        if assignment_form.is_valid():
            classroom = assignment_form.cleaned_data.get('classroom')
            assignment = assignment_form.save(commit=False)
            assignment.created_by = request.user
            assignment.course = classroom.course
            assignment.save()
            return redirect(reverse_lazy('assignment:assignment_list'))
        
        context = {
            'assignment_form': assignment_form,
        }
        
        return render(request, self.template_name, context)


class EditAssignmentView(LoginRequiredMixin, views.View):
    model = Assignment
    form_class = EditAssignmentForm
    template_name = 'assignment/assignment_edit.html'

    def get(self, request, pk, *args, **kwargs):
        assignment = get_object_or_404(self.model, pk=pk)

        assignment_form = self.form_class(initial={
            'classroom': assignment.classroom,
           'title': assignment.title,
           'details': assignment.details,
           'due_date': assignment.due_date,
           'close_date': assignment.close_date,
           'file': assignment.file,
           'points': assignment.points
        })
        return render(request, self.template_name, {
            "assignment_form": assignment_form
        })

    def post(self, request, pk, *args, **kwargs):
        assignment = get_object_or_404(self.model, pk=pk)

        assignment_form = self.form_class(request.POST, request.FILES)

        if assignment_form.is_valid():
            assignment.classroom = assignment_form.cleaned_data.get('classroom', 
                                                                    assignment.classroom)
            assignment.title = assignment_form.cleaned_data.get('title',
                                                               assignment.title)
            assignment.details = assignment_form.cleaned_data.get('details',
                                                               assignment.details)
            assignment.due_date = assignment_form.cleaned_data.get('due_date',
                                                                assignment.due_date)
            assignment.close_date = assignment_form.cleaned_data.get('close_date',
                                                            assignment.close_date)
            assignment.points = assignment_form.cleaned_data.get('points',
                                                                assignment.points)
            assignment.file = assignment_form.cleaned_data.get('file', assignment.file)
            assignment.created_by = request.user
            assignment.save()
            return redirect('assignment:assignment_list')

        return render(request, self.template_name, {
            "assignment_form": assignment_form
        })


class AssignmentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Assignment
    success_url = reverse_lazy("assignment:assignment_list")
    template_name = 'assignment/assignment_confirm_delete.html'



# class AssignmentSubmissionView(LoginRequiredMixin, generic.View):
#     model = AssignmentSubmission
#     template_name = 'assignment/assignment_detail.html'
#     form_class = AssignmentSubmitForm

#     def get(self, request, *args, **kwargs):
#         assignment_submit_form = self.form_class()
#         context = {
#             'assignment_submit_form': assignment_submit_form
#         }

#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         assignment_submit_form = self.form_class(request.POST,  request.FILES)
#         if assignment_submit_form.is_valid():
#             assignment_submit = assignment_submit_form.save(commit=False)
#             assignment_submit.created_by = request.user
#             assignment_submit.save()
#             return redirect('assignment:assignment_list')
        
#         context = {
#             'assignment_form': assignment_submit_form
#         }
        
#         return render(request, self.template_name, context)

@login_required
def assignment_detail(request, pk):
    template_name = 'assignment/assignment_detail.html'
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

@login_required
def submission_detail(request, pk):
    template_name = 'assignment/submission_detail.html'
    submission = get_object_or_404(AssignmentSubmission, id=pk)
    
    if submission.assignment_id.created_by == request.user:
        if request.method == "POST":
            return_form = AssignmentReturnForm(request.POST)
            if return_form.is_valid():                    
                try:
                    submission.grade = return_form.cleaned_data.get('grade', submission.grade)
                    submission.status = "returned"
                    if submission.grade > submission.assignment_id.points:

                        return HttpResponse(
                            "Grade cannot be greater than initial assignment points"
                        )
                    else:    
                        submission.save()
                        return redirect("assignment:assignment_list")
                except submission.grade > submission.assignment_id.points:
                    raise ValueError("Grade cannot be greater than assignment points")
        
        else:
            return_form = AssignmentReturnForm()
    else:
        return HttpResponseNotFound("Request Not Allowed")
    context = {
        'submission': submission,
        'return_form': return_form
    }

    return render(request, template_name, context)

