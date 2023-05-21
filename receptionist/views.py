from django.utils import timezone
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.views.decorators.http import require_POST
from client.models import Client
from main_home.forms import BloodTypeForm, UserRegisterForm

from main_home.models import Appointment, BloodBank, Complaint, Invoice, Lobby, Payment
from nurse.models import Nurse
from receptionist.forms import ConfirmationForm
from django.db.models import Count, Q
from django.contrib.auth.models import Group
# Create your views here.

################################################################

# Home Invoices

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def receptionist_home(request):
    invoices = Invoice.objects.all()
    
    context ={
        'invoices':invoices
    }
    return render(request,'receptionist/receptionist.html', context)

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def invoice_detail(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    payment = invoice.report.test_result.request.appointment.payment 
    unpaid = invoice.total_price - payment.total_amount_payed
    context ={
        'invoice':invoice,
        'payment':payment,
        'unpaid':unpaid
    }
    
    return render(request,'receptionist/invoice/invoice_detail.html', context)

def confirm_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == 'POST':
        appointment=invoice.report.test_result.request.appointment
        
        # Update the payment status of the invoice
        invoice.payment_status = True
        invoice.save()

        # Update the payment model with the amount paid
        payment = Payment.objects.get(appointment=appointment)
        payment.payed_nurse_tests_fee = True
        payment.total_amount_payed += (invoice.total_price-payment.total_amount_payed)
        payment.save()
        
        appointment.payment_status = True
        appointment.save()

        # Redirect to the invoice detail page

    return redirect('invoice_detail', invoice_id=invoice_id)
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
            user = form.save()
            # add him to the client group
            group = Group.objects.get(name="client")
            group.user_set.add(user)
            # extract form data
            data = form.cleaned_data
            phone_number = data.get("phone_number")
            gender = data.get("gender")
            address = data.get("address")
            policy = data.get("policy")
            date_of_birth = data.get("date_of_birth")
            # add him with any additionel information into the client table
            Client.objects.create(user = user,
                            phone_number = phone_number,
                            gender = gender,
                            address = address,
                            policy = policy,
                            date_of_birth = date_of_birth)
            
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
            #
            nurse = Nurse.objects.annotate(
                analysis_requests_count=Count('analysisrequest', filter=Q(analysisrequest__status__in=['pending', 'working-on']))
            ).order_by('analysis_requests_count').first()

            if nurse:
                lobby, _ = Lobby.objects.get_or_create(nurse=nurse)
                lobby.clients.add(appointment)
                
                
            appointment_fee_paid = form.cleaned_data["appointment_fee_paid"]
            tests_fee_paid = form.cleaned_data["tests_fee_paid"]
            
            if appointment_fee_paid:
                payment.total_amount_payed+=appointment_fee
                payment.payed_appointment_fee = True   
                
            if tests_fee_paid:
                payment.total_amount_payed+=tests_fee
                payment.payed_tests_fee = True
                
            if appointment_fee_paid and tests_fee_paid:
                appointment.payment_status = True   
                
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
