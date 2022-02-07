from django.urls import path
from . import views

app_name = 'assignment'
urlpatterns = [
    path('', views.AssignmentList.as_view(), name='assignment_list'),
    path('add/', views.AddAssignmentView.as_view(), name='add_assignment'),
    path('<int:pk>/edit/', views.EditAssignmentView.as_view(), name='edit_assignment'),
    path('<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('<int:pk>/delete', views.AssignmentDeleteView.as_view(), name='assignment_delete')
]