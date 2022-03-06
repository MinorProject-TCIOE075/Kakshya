from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>/', views.ClassroomList.as_view(), name='classroom_list'),
    path('cr/add/', views.CreateClassroomView.as_view(), name='classroom_add'),
    path('cr/<int:pk>/', views.ClassroomDetailView.as_view(), name='classroom_detail'),
    path('cr/post/<int:classroom_pk>/add/', views.CreatePostView.as_view(), name='post_add'),
    # path('cr/post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('cr/post/<int:pk>/edit', views.EditPostView.as_view(), name='post_edit'),
]