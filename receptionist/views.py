from django.utils import timezone
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.views.decorators.http import require_POST

from main_home.models import Appointment

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
    
    appointments = Appointment.objects.all()
    appointments_today = []
    appointments_tomorrow = []
    appointments_upcoming = []

    for appointment in appointments:
        if appointment.status == appointment.TODAY:
            appointments_today.append(appointment)
        elif appointment.status == appointment.TOMORROW:
            appointments_tomorrow.append(appointment)
        elif appointment.status == appointment.UPCOMING:
            appointments_upcoming.append(appointment)

    context = {
        'appointments_today': appointments_today,
        'appointments_tomorrow': appointments_tomorrow,
        'appointments_upcoming': appointments_upcoming,
    }

    
    return render(request,'receptionist/appointment/appointment_list.html',context)

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def appointment_detail(request,appointment_id):
    
    appointment = get_object_or_404(Appointment, id=appointment_id)

    context = {
        'appointment': appointment
    }
    
    return render(request,'receptionist/appointment/appointment_detail.html',context)

@require_POST
def mark_arrived(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.arrived = True
    appointment.save()
    return redirect('appointment_detail', appointment_id=appointment_id)

@require_POST
def cancel_arrived(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.arrived = False
    appointment.save()
    return redirect('appointment_detail', appointment_id=appointment_id)

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
