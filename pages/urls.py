from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path("<username>/", views.ProfileView.as_view(), name='profile'),
    path("<username>/edit/", views.ProfileEdit.as_view(), name='profile_edit'),
    path("", views.home, name="home"),
    path("routines/r/", views.DailyRoutineView.as_view(), name='daily_routine'),
    path("routines/r/<int:pk>", views.RoutineCourseView.as_view(), name='routine_course'),
    path("classroom/c/", views.ClassRoom.as_view(), name='classroom'),
    path("classroom/c/<int:pk>", views.ClassRoomView.as_view(), name='classroom_detail'),
    path("u/assignments/", views.StudentAssignment.as_view(), name='student_assignment'),
    path("u/assignments/<int:pk>", views.assignment_detail, name='assignment_detail')
]