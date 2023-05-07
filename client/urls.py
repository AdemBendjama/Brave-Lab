from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.client_home,name="client"),
]