from django.contrib import admin
from django.urls import path
from . import views
from main_home import views as home_views

urlpatterns = [
    path("",views.receptionist_home,name="receptionist"),
    path("invoice/<int:invoice_id>/",views.invoice_detail,name="invoice_detail"),
    path('invoice/<int:invoice_id>/confirm_payment/', views.confirm_payment, name='confirm_payment'),
    
    path("add/blood/",views.blood_add,name="blood_add"),
    path("add/client/",views.client_add,name="client_add"),
    
    path("appointment/list/",views.appointment_list,name="appointment_list"),
    path("appointment/detail/<int:appointment_id>/",views.appointment_detail,name="appointment_detail"),
    path("appointment/confirm/<int:appointment_id>/",views.appointment_confirm,name="appointment_confirm"),
    
    path("complaint/list/",views.complaint_list,name="complaint_list"),
    path("complaint/detail/<int:complaint_id>/",views.complaint_detail,name="complaint_detail"),
]