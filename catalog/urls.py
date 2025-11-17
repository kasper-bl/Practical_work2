from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.appliation_views, name='create_application'),
    path('user_application/', views.user_application, name='user_application')
]