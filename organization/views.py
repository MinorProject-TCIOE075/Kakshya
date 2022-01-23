from django.shortcuts import render

from .forms import ProgramForm, DepartmentForm


# Create your views here.
def add_program(request, *args, **kwargs):
    program_form = ProgramForm()
    department_form = DepartmentForm()
    if request.method == "POST":
        # program_form = ProgramForm(request.POST)
        # if program_form.is_valid():
        #     print("valid", program_form.cleaned_data)
        #     return render(request, "programform.html", {
        #         'program_form': ProgramForm(),
        #         'department_form': DepartmentForm()
        #     })

        department_form = DepartmentForm(request.POST)
        if department_form.is_valid():
            print("Valid => ", department_form.cleaned_data)
            return render(request, "programform.html", {
                'program_form': program_form,
                'department_form': DepartmentForm()
            })
        return render(request, "programform.html", {
            'program_form': program_form,
            'department_form': department_form
        })
    return render(request, 'programform.html', {
        'program_form': program_form,
        'department_form': department_form
    })
