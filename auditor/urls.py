from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.auditor_home,name="auditor"),
    
    path("message/message_chat/",views.message_chat,name="message_chat"),

    path("results/",views.result_list,name="result_list"),
    path("results/<int:result_id>/detail",views.result_detail,name="result_detail"),
    
    path("reports/",views.report_list,name="report_list"),
    path("reports/<int:report_id>/detail/",views.report_detail,name="report_detail"),
    path("reports/add/",views.report_add,name="report_add"),
]