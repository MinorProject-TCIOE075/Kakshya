from django.urls import path

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
    path('departments/d/<department_pk>/p/add', views.AddProgramView.as_view(),
         name='program_add'),
    path('departments/d/<department_pk>/p/<pk>/delete/', views.delete_program,
         name='program_delete')
]
