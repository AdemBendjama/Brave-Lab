from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.nurse_home,name="nurse"),
]