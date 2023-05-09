from django.contrib import admin
from django.urls import path
from . import views
from main_home import views as home_views

urlpatterns = [
    path("",views.client_home,name="client"),
    path("profile", home_views.profile_update ,name="profile_update"),
]