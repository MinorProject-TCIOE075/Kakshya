from django.urls import path
from . import views

app_name = 'assignment'
urlpatterns = [
    path('a/', views.AssignmentList.as_view(), name='assignment_list'),
    path('a/<int:classroom_pk>/add/', views.AddAssignmentView.as_view(), name='add_assignment'),
    path('a/<int:pk>/edit/', views.EditAssignmentView.as_view(), name='edit_assignment'),
    path('a/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('a/<int:pk>/delete', views.AssignmentDeleteView.as_view(), name='assignment_delete'),
    path('submission/<int:pk>/', views.submission_detail, name='submission_detail')
]