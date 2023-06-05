from django.contrib import admin
from .models import BloodSample, ChatRoom, Complaint, Laboratory, ComponentInformation, Component, Lobby, Message, Payment, TestOffered, Test, BloodBank, MedicalDocument, Appointment, AnalysisRequest, TestResult, Report, Invoice

# register your models here.
admin.site.register(Complaint)
admin.site.register(Laboratory)
admin.site.register(ComponentInformation)
admin.site.register(Component)
admin.site.register(TestOffered)
admin.site.register(Test)
admin.site.register(BloodBank)
admin.site.register(BloodSample)
admin.site.register(MedicalDocument)
admin.site.register(Appointment)
admin.site.register(AnalysisRequest)
admin.site.register(TestResult)
admin.site.register(Report)
admin.site.register(Invoice)
admin.site.register(Payment)
admin.site.register(Lobby)
admin.site.register(ChatRoom)
admin.site.register(Message)
