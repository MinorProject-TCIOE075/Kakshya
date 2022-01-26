from django.urls import path
from . import views

app_name = 'myadmin'
urlpatterns = [
    path('', views.AdminDashboard.as_view(), name='dashboard'),
]