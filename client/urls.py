from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.client_home,name="client"),
    
    path("help/",views.client_help,name="profile_help"),
    path("contact/",views.client_contact,name="profile_contact"),
    path("policy/",views.client_policy,name="profile_policy"),
    path("complaint/",views.create_complaint,name="create_complaint"),
    
    path("appointment/appointment_book",views.appointment_book,name="client_appointment_book"),
    path("appointment/appointment_confirm",views.appointment_confirm,name="client_appointment_confirm"),
    path("appointment/appointment_detail/<int:appointment_id>",views.appointment_detail,name="client_appointment_detail"),
    path("appointment/appointment_detail/<int:appointment_id>/cancel_appointment",views.cancel_appointment,name="client_cancel_appointment"),
    
    path("request/request_list",views.request_list,name="client_request_list"),
    path("request/request_detail",views.request_detail,name="client_request_detail"),
    
    path("result/result_list",views.result_list,name="client_result_list"),
    path("result/result_detail",views.result_detail,name="client_result_detail"),
]