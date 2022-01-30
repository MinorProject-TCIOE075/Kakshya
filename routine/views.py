from django.shortcuts import render

from .forms import DailyRoutineForm, CourseForm


def test_forms(request, *args, **kwargs):
    daily_routine_form = DailyRoutineForm()
    courses_form = CourseForm()
    if request.method == 'POST':
        daily_routine_form = DailyRoutineForm(request.POST)
        courses_form = CourseForm(request.POST)
        if daily_routine_form.is_valid():
            return render(request, 'test.html', {
                'daily_routine_form': DailyRoutineForm(),
                'courses_form': CourseForm()
            })
        if courses_form.is_valid():
            return render(request, 'test.html', {
                'daily_routine_form': DailyRoutineForm(),
                'courses_form': CourseForm()
            })
        return render(request, 'test.html', {
            'daily_routine_form': daily_routine_form,
            'courses_form': courses_form
        })

    return render(request, 'test.html', {
        'daily_routine_form': daily_routine_form,
        'courses_form': courses_form
    })
