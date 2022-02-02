from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListRoutineView.as_view(), name='routine_list')
]