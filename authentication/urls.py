from django.urls import path, re_path
from . import views
from .forms import *


"""
    named_signup_forms is a tuple which have the key and value for the multiple signup forms
    'Email and more' is the 1st signup form that is rendered when a user enters the url for sign up process
    After submitting the SignUpFormOne the user is prompted to the second form namely SingUpFormTwo
    after both the form is submitted the details are recorded and saved in the database under the User model.
"""
named_signup_forms = (
    ('Email and more', SignUpFormOne),
    ('Personal Information', SignUpFormTwo)
)

"""
    signup_form is a variable created simply to simplify and make the url path cleaner.
    this variable is passed as the view for the url path named re_path('signup/(?P<step>.+)$', ...)
"""
signup_form = views.FormWizardView.as_view(named_signup_forms,
    url_name='auth:signup', done_step_name='finished')



app_name = 'auth'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),

    # These following 4 paths are for the password reset functionality although it is not ready yet.

    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # The following two paths arefor the signup functionality
    # The re_path checks the relative expression of the url path and if valid renders the signup_form view
    re_path(r'^signup/(?P<step>.+)$', signup_form, name='signup'),
    # 

    path('signup/', signup_form, name='signup'),

    # update urls
    path('teacher-update/', views.UpdateTeacherProfile, name='teacher-profile-update'),
    # path('student-update/', views.StudentProfileUpdate, name = 'student-update')
]