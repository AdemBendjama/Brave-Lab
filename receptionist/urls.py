from django.contrib import admin
from django.urls import path
from . import views
from main_home import views as home_views

urlpatterns = [
    path("",views.receptionist_home,name="receptionist"),
]