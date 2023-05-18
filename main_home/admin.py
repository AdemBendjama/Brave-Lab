from django.contrib import admin
from .models import Complaint, Laboratory, ComponentInformation, Component, Payment, TestOffered, Test, BloodBank, MedicalDocument, Appointment, AnalysisRequest, TestResult, Report, Invoice

# register your models here.
admin.site.register(Complaint)
admin.site.register(Laboratory)
admin.site.register(ComponentInformation)
admin.site.register(Component)
admin.site.register(TestOffered)
admin.site.register(Test)
admin.site.register(BloodBank)
admin.site.register(MedicalDocument)
admin.site.register(Appointment)
admin.site.register(AnalysisRequest)
admin.site.register(TestResult)
admin.site.register(Report)
admin.site.register(Invoice)
admin.site.register(Payment)
