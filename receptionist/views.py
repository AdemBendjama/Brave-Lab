from django.utils import timezone
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.views.decorators.http import require_POST
from client.models import Client
from main_home.forms import BloodTypeForm, UserRegisterForm

from main_home.models import Appointment, BloodBank, Complaint
from receptionist.forms import ConfirmationForm

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
    if request.method == 'POST' and 'add' in request.POST:
        form = BloodTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receptionist')
    elif request.method == 'POST' and 'update' in request.POST:
        bloodbank = BloodBank.objects.get(client = request.POST.get("client"))
        bloodbank.blood_type = request.POST.get("blood_type")
        bloodbank.save()
        return redirect('receptionist')
    
    else:
        form = BloodTypeForm()
    
    context = {
        'form': form
    }
    return render(request,'receptionist/add/blood_add.html',context)

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def client_add(request):
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('receptionist')
    else:
        form = UserRegisterForm()
    
    context = {
        'form': form
    }
    
    return render(request,'receptionist/add/client_add.html',context)

################################################################

# Appointments

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def appointment_list(request):
    
    appointments = Appointment.objects.exclude(cancelled=True)
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


@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def appointment_confirm(request, appointment_id):
    
    appointment = Appointment.objects.get(id=appointment_id)
    payment = appointment.payment
    tests_fee = payment.tests_fee
    appointment_fee = payment.appointment_fee
    
    if request.method == 'POST':
        form = ConfirmationForm(request.POST, tests_fee=tests_fee, appointment_fee=appointment_fee)
        if form.is_valid():
            appointment_fee_paid = form.cleaned_data["appointment_fee_paid"]
            tests_fee_paid = form.cleaned_data["tests_fee_paid"]
            
            if appointment_fee_paid:
                payment.total_amount_payed+=appointment_fee
                payment.payed_appointment_fee = True   
                
            if tests_fee_paid:
                payment.total_amount_payed+=tests_fee
                payment.payed_tests_fee = True   
                
            appointment.arrived = True
            
            payment.save()
            appointment.save()
            
            return redirect("appointment_detail",appointment_id=appointment_id)
                
    else:
        form = ConfirmationForm(tests_fee=tests_fee, appointment_fee=appointment_fee)

    context={
        'form': form, 
        'appointment': appointment
    }
    
    return render(request,'receptionist/appointment/appointment_confirm.html',context)

################################################################

# Complaints 

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def complaint_list(request):
    complaints = Complaint.objects.all()
    context = {
        'complaints': complaints
    }
    
    return render(request,'receptionist/complaint/complaint_list.html',context)

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def complaint_detail(request,complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    context = {
        'complaint': complaint
    }
    return render(request,'receptionist/complaint/complaint_detail.html',context)

################################################################
