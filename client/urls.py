from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.client_home,name="client"),
    path("help/",views.client_help,name="profile_help"),
    path("contact/",views.client_contact,name="profile_contact"),
    path("policy/",views.client_policy,name="profile_policy"),
    path("complaint/",views.create_complaint,name="create_complaint"),
]