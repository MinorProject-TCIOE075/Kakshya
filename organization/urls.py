from django.urls import path

from classroom import views as classroom_views
from . import views

urlpatterns = [
    path('departments/', views.DepartmentListView.as_view(),
         name='department_list'),
    path('departments/d/add/', views.AddDepartmentView.as_view(),
         name='add_department'),
    path('departments/d/<pk>/', views.DepartmentView.as_view(),
         name='department'),
    path('departments/d/<pk>/edit/', views.EditDepartmentView.as_view(),
         name='department_edit'),
    path('departments/d/<pk>/delete/', views.delete_department,
         name='department_delete'),
    path('departments/d/<department_pk>/p/<pk>/',
         views.ProgramDetailView.as_view(), name='program'),
    path('departments/d/<department_pk>/p/add/',
         views.AddProgramView.as_view(),
         name='program_add'),
    path('departments/d/<department_pk>/p/<pk>/delete/', views.delete_program,
         name='program_delete'),
    path('departments/d/<department_pk>/p/<pk>/edit/',
         views.EditProgramView.as_view(),
         name='program_edit'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/add/', views.AddCourseView.as_view(), name='course_add'),
    path('courses/c/<int:pk>/', views.CourseDetailView.as_view(),
         name='course'),
    path('courses/c/<int:pk>/edit/', views.EditCourseView.as_view(),
         name='course_edit'),
    path('courses/c/<int:pk>/delete/', views.delete_course,
         name='course_delete'),

    # Paths related to classrooms and operations in admin page
    path('departments/d/<department_pk>/p/<program_pk>/cr/add/',
         classroom_views.CreateClassroomView.as_view(), name='classroom_add'),
    path('departments/d/<department_pk>/p/<program_pk>/cr/<pk>/edit/',
         classroom_views.EditClassroomView.as_view(), name='classroom_edit'),
    path('departments/d/<department_pk>/p/<program_pk>/cr/<pk>/archive/',
         classroom_views.archive_classroom, name='classroom_archive'),
    path('departments/d/<department_pk>/p/<program_pk>/cr/<pk>/delete/',
         classroom_views.delete_classroom, name='classroom_delete'),
]
