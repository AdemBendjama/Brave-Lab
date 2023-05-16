from django.shortcuts import render
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.

################################################################

# Home Invoices

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def receptionist_home(request):
    
    return render(request,'receptionist/receptionist.html')

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def invoice_detail(request):
    
    return render(request,'receptionist/invoice/invoice_detail.html')

################################################################

# Creation Views (Client,Blood Samples)

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def blood_add(request):
    
    return render(request,'receptionist/add/blood_add.html')

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def client_add(request):
    
    return render(request,'receptionist/add/client_add.html')

################################################################

# Appointments

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def appointment_list(request):
    
    return render(request,'receptionist/appointment/appointment_list.html')

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def appointment_detail(request):
    
    return render(request,'receptionist/appointment/appointment_detail.html')

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def appointment_confirm(request):
    
    return render(request,'receptionist/appointment/appointment_confirm.html')

################################################################

# Complaints 

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def complaint_list(request):
    
    return render(request,'receptionist/complaint/complaint_list.html')

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def complaint_detail(request):
    
    return render(request,'receptionist/complaint/complaint_detail.html')

################################################################
