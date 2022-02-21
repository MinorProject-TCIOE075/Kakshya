from django.urls import path
from . import views

urlpatterns = [
    path('invite/', views.InvitationView.as_view(), name='invite_user'),
]