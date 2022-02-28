from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClassroomList.as_view(), name='classroom_list')
]