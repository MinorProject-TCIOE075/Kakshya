from django.urls import path

from . import views

urlpatterns = [
    path('invite/', views.InvitationView.as_view(), name='invite_user'),
    path('', views.UserListView.as_view(), name='user_list'),
    path('<username>/', views.UserDetailView.as_view(), name='user_detail'),
    path('<username>/edit/', views.UserEditView.as_view(), name='user_edit'),
    path('<username>/perms/', views.UserPermissionUpdateView.as_view(),
         name='user_permissions'),
    path('<username>/delete/', views.delete_user, name='user_delete')
]