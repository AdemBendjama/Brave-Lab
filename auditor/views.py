from django.shortcuts import render
from django.contrib.auth.decorators import login_required , permission_required

# Create your views here.

@login_required
@permission_required('auditor.view_auditor', raise_exception=True)
def auditor_home(request):
    
    return render(request,'auditor/auditor.html')