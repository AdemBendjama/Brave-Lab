from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.client_home,name="client"),
    
    path("help/",views.client_help,name="profile_help"),
    path("contact/",views.client_contact,name="profile_contact"),
    path("policy/",views.client_policy,name="profile_policy"),
    path("complaint/",views.create_complaint,name="create_complaint"),
    
    path("appointment/appointment_book",views.appointment_book,name="appointment_book"),
    path("appointment/appointment_confirm",views.appointment_confirm,name="appointment_confirm"),
    path("appointment/appointment_detail",views.appointment_detail,name="appointment_detail"),
    
    path("request/request_list",views.request_list,name="request_list"),
    path("request/request_detail",views.request_detail,name="request_detail"),
    
    path("result/result_list",views.result_list,name="result_list"),
    path("result/result_detail",views.result_detail,name="result_detail"),
]