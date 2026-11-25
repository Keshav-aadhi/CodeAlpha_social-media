from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
]
