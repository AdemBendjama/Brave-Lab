from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("",views.nurse_home,name="nurse"),
    path("lobby/<int:appointment_id>/detail/",views.lobby_detail,name="lobby_detail"),
   
    path("message/chat/",views.message_chat,name="nurse_message_chat"),
    
    path("requests/",views.request_list,name="request_list"),
    path("requests/<int:analysis_request_id>/detail/",views.request_detail,name="request_detail"),
    path('requests/<int:analysis_request_id>/start-analysis/', views.start_analysis, name='start_analysis'),
    path('requests/<int:analysis_request_id>/finish-analysis/', views.finish_analysis, name='finish_analysis'),
    
    
    path("requests/<int:analysis_request_id>/tests/",views.request_test_list,name="request_test_list"),
    path("requests/<int:analysis_request_id>/tests/add/",views.request_test_add,name="request_test_add"),
    path("requests/<int:analysis_request_id>/tests/<int:test_id>/add/components",views.request_test_add_component,name="request_test_add_component"),
    path("requests/tests/<int:test_id>/detail/",views.request_test_detail,name="request_test_detail"),
    
    path("results/",views.result_list,name="result_list"),
    path("results/<int:result_id>/detail/",views.result_detail,name="result_detail"),
    
]