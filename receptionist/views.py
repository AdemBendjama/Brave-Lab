from django.shortcuts import render
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def receptionist_home(request):
    
    return render(request,'receptionist/receptionist.html')