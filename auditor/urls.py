from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.auditor_home,name="auditor"),
    
    path("message/message_chat",views.message_chat,name="message_chat"),

    path("result/result_list",views.result_list,name="result_list"),
    path("result/result_detail",views.result_detail,name="result_detail"),
    
    path("report/report_list",views.report_list,name="report_list"),
    path("report/report_detail",views.report_detail,name="report_detail"),
    path("report/report_add",views.report_add,name="report_add"),
]