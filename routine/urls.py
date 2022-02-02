from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListRoutineView.as_view(), name='routine_list'),
    path('add/', views.AddRoutineView.as_view(), name='routine_add')
]