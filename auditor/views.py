from django.shortcuts import render
from django.contrib.auth.decorators import login_required , permission_required

# Create your views here.

################################################################

# Home - Stats

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def auditor_home(request):
    
    return render(request,'auditor/auditor.html')

################################################################

# Chat

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def message_chat(request):
    
    return render(request,'auditor/message/message_chat.html')

################################################################

# Results

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def result_list(request):
    
    return render(request,'auditor/result/result_list.html')

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def result_detail(request):
    
    return render(request,'auditor/result/result_detail.html')

################################################################

# Reports

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def report_list(request):
    
    return render(request,'auditor/report/report_list.html')

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def report_detail(request):
    
    return render(request,'auditor/report/report_detail.html')

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def report_add(request):
    
    return render(request,'auditor/report/report_add.html')