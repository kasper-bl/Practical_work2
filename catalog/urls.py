from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.application_views, name='create_application'),
    path('user_application/', views.user_application, name='user_application'),
    path('delete_application/<int:pk>/', views.delete_application, name='delete_application'),
    path('admin/applications/', views.admin_applications, name='admin_applications'),
    path('admin/application/<int:pk>/change_status/', views.change_status, name='change_status'),
]