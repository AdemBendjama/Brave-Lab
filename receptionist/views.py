from django.utils import timezone
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.decorators import login_required,permission_required
from django.views.decorators.http import require_POST
from .forms import AppointmentForm
from client.models import Client
from main_home.forms import UserRegisterForm

from main_home.models import Appointment, BloodBank, Complaint, Invoice, Lobby, Payment, Report
from nurse.models import Nurse
from receptionist.forms import ConfirmationForm
from django.db.models import Count, Q
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from brave_lab_project.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from django.core.files.storage import default_storage
# Create your views here.

################################################################

# Home Invoices

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def receptionist_home(request):
    reports = Report.objects.all()
    
    context ={
        'reports':reports
    }
    return render(request,'receptionist/receptionist.html', context)

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def receptionist_report_detail(request,report_id):
    report = Report.objects.get(id=report_id)
    context ={
        'report':report,
    }
    
    return render(request,'receptionist/report/report_detail.html', context)
    

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def invoice_detail(request, report_id, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    payment = invoice.report.test_result.request.appointment.payment 
    unpaid = invoice.total_price - payment.total_amount_payed
    context ={
        'invoice':invoice,
        'payment':payment,
        'unpaid':unpaid
    }
    
    return render(request,'receptionist/invoice/invoice_detail.html', context)

def confirm_payment(request,report_id , invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == 'POST':
        appointment=invoice.report.test_result.request.appointment
        
        # Update the payment status of the invoice
        invoice.payment_status = True
        invoice.save()

        # Update the payment model with the amount paid
        payment = Payment.objects.get(appointment=appointment)
        payment.payed_nurse_tests_fee = True
        payment.payed_tests_fee = True
        payment.total_amount_payed += invoice.total_price
        payment.save()
        
        appointment.payment_status = True
        appointment.save()

        # Redirect to the invoice detail page

    return redirect('invoice_detail',report_id=report_id, invoice_id=invoice_id)
################################################################


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


@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def appointment_add(request):
    
    if request.method == 'POST' :
        form = AppointmentForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            date = date.strftime("%Y-%m-%d")
            description = form.cleaned_data['description']
            tests_requested = form.cleaned_data['tests_requested']
            
            if 'document' in request.FILES :
                document_file = request.FILES['document']
                document = default_storage.save('medical_documents/' + document_file.name, document_file)
            else :
                document = None
            urgent=False
            total_price = 0
            for test in tests_requested:
                if test.urgent :
                    urgent = True
                total_price+=test.price
            
            client = form.cleaned_data['client']
            
            appointment = Appointment()
            appointment.client = client
            appointment.date = date
            appointment.description = description
            if document :
                appointment.document = document
            appointment.total_price = total_price
            appointment.urgent = urgent
            appointment.save()
            
            appointment.tests_requested.add(*tests_requested)
            
            payment = Payment(appointment=appointment)
            payment.save()
            
            payment.tests_fee = appointment.total_price
            
            payment.save()
            appointment.save()
            
            return redirect('appointment_detail',appointment_id=appointment.id)
    else:
        form = AppointmentForm() 
       
    
        
    context={
        'form':form,
    }
         
    return render(request,'receptionist/add/appointment_add.html',context)

################################################################

# Appointments

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def appointment_list(request):
    
    appointments = Appointment.objects.exclude(cancelled=True)
    appointments_today = []
    appointments_tomorrow = []
    appointments_upcoming = []
    paid_appointments = []

    for appointment in appointments:
        if appointment.payment.payed_appointment_fee and appointment.arrived:
            paid_appointments.append(appointment)
        elif appointment.status == appointment.TODAY:
            appointments_today.append(appointment)
        elif appointment.status == appointment.TOMORROW:
            appointments_tomorrow.append(appointment)
        elif appointment.status == appointment.UPCOMING:
            appointments_upcoming.append(appointment)

    context = {
        'appointments_today': appointments_today,
        'appointments_tomorrow': appointments_tomorrow,
        'appointments_upcoming': appointments_upcoming,
        'paid_appointments': paid_appointments,
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
    appointment_fee = payment.appointment_fee
    
    if request.method == 'POST':
        form = ConfirmationForm(request.POST, appointment_fee=appointment_fee)
        if form.is_valid():
            #
            payed = request.POST.get("payed")
            nurse = Nurse.objects.annotate(
                analysis_requests_count=Count('analysisrequest', filter=Q(analysisrequest__status__in=['pending', 'working-on']))
            ).order_by('analysis_requests_count').first()

            if nurse:
                lobby, _ = Lobby.objects.get_or_create(nurse=nurse)
                lobby.clients.add(appointment)
                
                
            appointment_fee_paid = form.cleaned_data["appointment_fee_paid"]
            
            if appointment_fee_paid and payed != "payed":
                print("appointment payed through form")
                payment.total_amount_payed+=appointment_fee
                payment.payed_appointment_fee = True   
                
            appointment.arrived = True
            
            payment.save()
            appointment.save()
            
            
            
            return redirect("appointment_detail",appointment_id=appointment_id)
                
    else:
        form = ConfirmationForm(appointment_fee=appointment_fee)

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


## reply to complaint 

@login_required
@permission_required('receptionist.view_receptionist', raise_exception=True)
def reply_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    client=complaint.client
    if request.method == 'POST':
        content = request.POST.get("description")
        title = f"{complaint.topic}"
        topic = f"Replying to Customer Complaint No.{complaint_id}"
        subject = f'{ client.user.first_name } { client.user.last_name } Customer Complaint Reply'
        
        html = render_to_string('receptionist/complaint/complaint_email_template.html',{
            "user":request.user,
            "topic":topic,
            'content':content,
            'title':title,
        })
        
        send_mail(subject,content ,EMAIL_HOST_USER,[f"{client.user.email}"],html_message=html)
        
        return redirect('complaint_detail',complaint_id=complaint_id)
        

    return render(request, 'receptionist/complaint/complaint_detail.html')