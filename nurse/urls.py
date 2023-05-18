from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.nurse_home,name="nurse"),
    path("lobby/lobby_detail/<int:appointment_id>",views.lobby_detail,name="lobby_detail"),
   
    path("message/message_chat",views.message_chat,name="nurse_message_chat"),
    
    path("request/request_list",views.request_list,name="request_list"),
    path("request/request_detail",views.request_detail,name="request_detail"),
    
    path("request/test/request_test_add",views.request_test_add,name="request_test_add"),
    path("request/test/request_test_detail",views.request_test_detail,name="request_test_detail"),
    path("request/test/request_test_list",views.request_test_list,name="request_test_list"),
]