from django.urls import path
from . import views


urlpatterns = [
    path('', views.ClassroomList.as_view(), name='classroom_list'),
    path('cr/add/', views.CreateClassroomView.as_view(), name='classroom_add'),
    path('cr/<int:pk>/', views.ClassroomDetailView.as_view(), name='classroom_detail'),
    path('cr/post/add/', views.CreatePostView.as_view(), name='post_add'),
]