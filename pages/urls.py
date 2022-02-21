from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path("<username>/", views.ProfileView.as_view(), name='profile'),
    path("<username>/edit/", views.ProfileEdit.as_view(), name='profile_edit'),
]