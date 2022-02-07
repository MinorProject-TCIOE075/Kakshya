from django import views
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AssignmentForm, EditAssignmentForm
from .models import Assignment, AssignmentSubmission


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
            assignment = assignment_form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            return redirect('assignment:assignment_list')
        
        context = {
            'assignment_form': assignment_form
        }
        
        return render(request, self.template_name, context)


class EditAssignmentView(LoginRequiredMixin, views.View):
    model = Assignment
    form_class = EditAssignmentForm
    template_name = 'assignment/assignment_edit.html'

    def get(self, request, pk, *args, **kwargs):
        assignment = get_object_or_404(self.model, pk=pk)

        assignment_form = self.form_class(initial={
           
        })
        return render(request, self.template_name, {
            "assignment_form": assignment_form
        })

    def post(self, request, pk, *args, **kwargs):
        assignment = get_object_or_404(self.model, pk=pk)

        assignment_form = self.form_class(request.POST, request.FILES)

        if assignment_form.is_valid():
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


class AssignmentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Assignment
    template_name = 'assignment/assignment_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AssignmentDetailView, self).get_context_data(*args, **kwargs)

        return context


class AssignmentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Assignment
    success_url = reverse_lazy("assignment:assignment_list")
    template_name = 'assignment/assignment_confirm_delete.html'