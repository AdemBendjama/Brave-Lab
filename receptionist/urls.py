from django.contrib import admin
from django.urls import path
from . import views
from main_home import views as home_views

urlpatterns = [
    path("",views.receptionist_home,name="receptionist"),
    path("invoice/invoice_detail",views.invoice_detail,name="invoice_detail"),
    
    path("add/blood_add",views.blood_add,name="blood_add"),
    path("add/client_add",views.client_add,name="client_add"),
    
    path("appointment/appointment_list",views.appointment_list,name="appointment_list"),
    path("appointment/appointment_detail/<int:appointment_id>/",views.appointment_detail,name="appointment_detail"),
    path("appointment/appointment_confirm",views.appointment_confirm,name="appointment_confirm"),
    path('appointment/appointment_detail/<int:appointment_id>/mark_arrived', views.mark_arrived, name='mark_arrived'),
    path('appointment/appointment_detail/<int:appointment_id>/cancel_arrived', views.cancel_arrived, name='cancel_arrived'),
    
    path("complaint/complaint_list",views.complaint_list,name="complaint_list"),
    path("complaint/complaint_detail/<int:complaint_id>",views.complaint_detail,name="complaint_detail"),
]