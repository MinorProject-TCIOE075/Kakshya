from django.urls import path

from . import views

app_name = 'auth'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),

    # These following 4 paths are for the password reset functionality
    # although it is not ready yet.

    path('password_reset/', views.CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done', views.CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/', views.CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # Sign Up
    path('signup/<invitation_token>/', views.SignUpView.as_view(), name='signup'),


    # update urls
    path('teacher-update/', views.UpdateTeacherProfile,
         name='teacher-profile-update'),
]
