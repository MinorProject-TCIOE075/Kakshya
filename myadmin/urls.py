from django.urls import path, include
from . import views

app_name = 'myadmin'
urlpatterns = [
    path('', views.AdminDashboard.as_view(), name='dashboard'),
    path('org/', include('organization.urls')),
    path('routines/', include('routine.urls')),
    path('users/', include('myadmin.user_urls')),
    path('classroom/', include('classroom.urls'))
]