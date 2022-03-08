from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path("<username>/", views.ProfileView.as_view(), name='profile'),
    path("<username>/edit/", views.ProfileEdit.as_view(), name='profile_edit'),
    path("dashboard/", views.Dashboard.as_view(), name="dashboard"),
    path("routines/", views.DailyRoutineView.as_view(), name='daily_routine'),
    path("routines/r/<int:pk>", views.RoutineCourseView.as_view(), name='routine_course'),
    path("classroom/", views.ClassRoom.as_view(), name='classroom'),
    path("classroom/cr/<int:pk>", views.ClassRoomView.as_view(), name='classroom_detail'),
    path("u/assignments/", views.StudentAssignment.as_view(), name='student_assignment'),
    path("u/assignments/as/<int:pk>", views.assignment_detail, name='assignment_detail'),
    path("files/shared", views.SharedFiles.as_view(), name="shared_files"),
    path("classroom/cr/<int:pk>/assignments/add", views.AddAssignmentView.as_view(), name='add_assignment'),
    path("classroom/cr/<int:classroom_pk>/post/add", views.AddPostView.as_view(), name='post_add'),
    path("classroom/cr/<int:classroom_pk>/post/<int:post_pk>", views.PostDetail.as_view(), name='post_detail'),
    path("assignments/<int:pk>/submission", views.submission_detail, name='submission_detail')
]