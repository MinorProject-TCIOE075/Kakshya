from django.urls import path

from . import views

# app_name = 'organization'
urlpatterns = [
    path('departments/', views.DepartmentListView.as_view(),
         name='department_list'),
    path('departments/d/add/', views.AddDepartmentView.as_view(),
         name='add_department'),
    path('departments/d/<pk>/', views.DepartmentView.as_view(),
         name='department'),
]
