from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListRoutineView.as_view(), name='routine_list'),
    path('add/', views.AddRoutineView.as_view(), name='routine_add'),
    path('r/<int:pk>/', views.DetailRoutineView.as_view(), name='routine'),
    path('r/<int:pk>/edit/', views.EditRoutineView.as_view(),
         name='routine_edit'),
    path('r/<int:pk>/delete/', views.delete_routine,
         name='routine_delete'),
    path('r/<int:pk>/course/add/', views.AddRoutineCourseView.as_view(),
         name='routine_course_add'),
    path('r/<int:routine_pk>/course/<int:pk>/edit/',
         views.EditRoutineCourseView.as_view(),
         name='routine_course_edit'),
]
