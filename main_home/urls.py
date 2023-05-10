from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('' , views.home , name="home" ),
    path('register/' , views.register , name="register" ),
    path('login/' , views.login_view , name="login" ),
    path('logout/' ,auth_views.LogoutView.as_view(template_name="main_home/logout.html")  , name="logout" ),
    path('profile/',views.profile_update,name="profile_update"),
    
]