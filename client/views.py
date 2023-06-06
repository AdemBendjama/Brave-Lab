from datetime import datetime
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404, render ,redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required , permission_required
from django.template.loader import render_to_string
from brave_lab_project.settings import EMAIL_HOST_USER
from main_home.models import Appointment, Complaint, Invoice, MedicalDocument, Payment, TestOffered
from .forms import  AppointmentForm, AppointmentPaymentForm, ClientContactForm, ComplaintForm
from django.core.files.storage import default_storage
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages

# Create your views here.

################################################################

# Home

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_home(request):
    # 
    appointments = Appointment.objects.filter(client=request.user.client).order_by('date')

    active_appointments = []
    canceled_appointments = []
    overdue_appointments = []

    for appointment in appointments:
        if appointment.cancelled:
            canceled_appointments.append(appointment)
        elif appointment.status == appointment.OVERDUE:
            overdue_appointments.append(appointment)
        else:
            active_appointments.append(appointment)

    context = {
        'active_appointments': active_appointments,
        'canceled_appointments': canceled_appointments,
        'overdue_appointments': overdue_appointments,
    }
    return render(request,'client/client.html',context)

################################################################

# Appointment

@login_required
@permission_required('client.view_client', raise_exception=True)
def appointment_book(request):
        
    form = AppointmentForm()   
         
    return render(request,'client/appointment/appointment_book.html',{'form':form})

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_appointment_confirm(request):
    
    if request.method == 'POST':
        
        if request.POST.get("date") :
            
            form = AppointmentForm(request.POST,request.FILES)
            
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
                
                total_price = 0
                for test in tests_requested:
                    total_price+=test.price
                
                data = {
                    'date':date,
                    'description':description,
                    'document':document,
                    'tests_requested':tests_requested,
                    'total_price':total_price,
                }
                
                print(f'{type(date)} _ {description} _ {tests_requested} _ {total_price} _ {document} ')
                
            else:
                return render(request,'client/appointment/appointment_book.html',{'form':form})
            
        elif request.POST.get("payed") :
            
            form = AppointmentPaymentForm(request.POST)
            
            if form.is_valid:
                client = request.user.client
                
                tests_requested=[]
                test_count = int(request.POST.get("data.test_count"))
                for i in range(1,test_count+1):
                    test_id = int(request.POST.get(f"data.tests_requested{i}"))
                    test = TestOffered.objects.get(id=test_id)
                    tests_requested.append(test)
                    
                date = datetime.strptime(request.POST.get("data.date"), "%Y-%m-%d").date()
                description = request.POST.get('data.description')
                if "data.document" in request.POST:
                    document = request.POST.get('data.document')
                    doc_was_provided=True
                else:
                    doc_was_provided=False
                    
                total_price = Decimal(request.POST.get('data.total_price'))
                
                appointment = Appointment()
                appointment.client = client
                appointment.date = date
                appointment.description = description
                if doc_was_provided :
                    appointment.document = document
                appointment.total_price = total_price
                appointment.save()

                # Add the tests_requested to the appointment
                appointment.tests_requested.add(*tests_requested)
                
                # 
                payment = Payment(appointment=appointment)
                payment.save()
                
                payment.tests_fee = appointment.total_price
                
                payment.save()
                appointment.save()
                
                return redirect('client_appointment_contract',appointment_id=appointment.id)
            else:
                redirect('client_appointment_book')
                
    else:
        return redirect('client_appointment_book')

    context ={
        'data':data,
    }

    return render(request,'client/appointment/appointment_confirm.html',context)

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_appointment_contract(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    payment = appointment.payment
    
    if request.method == 'POST' and "confirm" in request.POST:
        return redirect('client_appointment_pay',appointment_id=appointment_id)
    if request.method == 'POST' and "cancel" in request.POST:
        appointment.delete()
        payment.delete()
        return redirect("client")

    context = {
        "appointment":appointment,
    }

    return render(request,'client/appointment/appointment_contract.html',context)

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_appointment_pay(request, appointment_id):
    
    if request.method == 'POST':
        payed = request.POST.get('payed')
        if payed == 'payed':
            appointment = Appointment.objects.get(id=appointment_id)
            payment = appointment.payment
            payment.total_amount_payed += payment.appointment_fee
            payment.payed_appointment_fee = True
            
            payment.save()
            
        messages.success(request, 'Appointment Booked successfully!')
            
        return redirect('client')
        

    return render(request,'client/appointment/appointment_pay.html')

@login_required
@permission_required('client.view_client', raise_exception=True)
def appointment_detail(request, appointment_id):
    # Retrieve the appointment based on the provided ID
    appointment = get_object_or_404(Appointment, id=appointment_id)
    time_difference = appointment.date - timezone.now().date()
    context = {
        'appointment': appointment,
        'time_difference': time_difference.days,
    }
    
    return render(request,'client/appointment/appointment_detail.html',context)


@login_required
@permission_required('client.view_client', raise_exception=True)
def cancel_appointment(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        time_difference = appointment.date - timezone.now().date()
        if time_difference >= timedelta(days=3):
            # Cancel appointment logic here
            appointment.cancelled = True
            appointment.save()
            messages.success(request, "Appointment successfully cancelled.")
        else:
            messages.error(request, "Cannot cancel appointment. Less than 3 days remaining.")
    else:
        messages.error(request, "Invalid request.")
    
    return redirect('client_appointment_detail', appointment_id=appointment_id)

################################################################

# Request

@login_required
@permission_required('client.view_client', raise_exception=True)
def request_list(request):
    appointments = Appointment.objects.filter(cancelled=False)
    
    context = {
        'appointments': appointments
    }
    return render(request,'client/request/request_list.html',context)

@login_required
@permission_required('client.view_client', raise_exception=True)
def request_detail(request):
    
    
    return render(request,'client/request/request_detail.html')

################################################################

# Result

@login_required
@permission_required('client.view_client', raise_exception=True)
def result_list(request):
    invoices = Invoice.objects.filter(client=request.user.client, payment_status=True).all()
    unpaid_invoices = Invoice.objects.filter(client=request.user.client, payment_status=False).all()

    context = {
        'invoices': invoices,
        'unpaid_invoices': unpaid_invoices
    }
    
    return render(request,'client/result/result_list.html', context)

@login_required
@permission_required('client.view_client', raise_exception=True)
def result_detail(request, invoice_id):
    
    invoice = Invoice.objects.get(id=invoice_id)
    test_result = invoice.report.test_result
    test_request = test_result.request
    appointment = test_request.appointment
    
    context = {
        "invoice":invoice,
        "test_result":test_result,
        "test_request":test_request,
        "appointment":appointment
    }
    
    return render(request,'client/result/result_detail.html' , context )



    
@login_required
@permission_required('client.view_client', raise_exception=True)
def online_pay(request, invoice_id):
    
    invoice = Invoice.objects.get(id=invoice_id)
    test_result = invoice.report.test_result
    test_request = test_result.request
    appointment = test_request.appointment
    
    if request.method == "POST":
        appointment=invoice.report.test_result.request.appointment
        
        # Update the payment status of the invoice
        invoice.payment_status = True
        invoice.save()

        # Update the payment model with the amount paid
        payment = appointment.payment
        payment.payed_nurse_tests_fee = True
        payment.payed_tests_fee = True
        payment.total_amount_payed += invoice.total_price
        payment.save()
        
        appointment.payment_status = True
        appointment.save()
        
        return redirect("client_result_list")
    
    context = {
        "invoice":invoice,
        "test_result":test_result,
        "test_request":test_request,
        "appointment":appointment
    }
    
    return render(request,'client/result/online_pay.html' , context )

################################################################

# Profile

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_help(request):
    
    return render(request,'client/profile/help.html')

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_contact(request):
     
    if request.method == 'POST':
        form = ClientContactForm(request.POST)
        
        if form.is_valid():
            
            content = form.cleaned_data["content"]
            subject = f'{ request.user.first_name } { request.user.last_name } is Requesting Support';
            
            html = render_to_string('client/profile/contact_email_template.html',{
                "user":request.user,
                'content':content
            })
            
            send_mail(subject,content ,EMAIL_HOST_USER,["bravelaboratory2023@gmail.com"],html_message=html)
            return redirect('client')
        
    else:
        form = ClientContactForm()
        
    context = {
        'form':form,
    }
    
    return render(request,'client/profile/contact.html',context)

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_policy(request):
    
    return render(request,'client/profile/policy.html')

################################################################

# Complaint

@login_required
@permission_required('client.view_client', raise_exception=True)
def create_complaint(request):
    
    if request.method == 'POST':
        
        form = ComplaintForm(request.POST)
        
        if form.is_valid():
            
            content = form.cleaned_data["description"]
            topic = form.cleaned_data["topic"]
            subject = f'{ request.user.first_name } { request.user.last_name } Customer Complaint';
            
            html = render_to_string('client/complaint/complaint_email_template.html',{
                "user":request.user,
                "topic":topic,
                'content':content,
            })
            
            complaint = Complaint(client = request.user.client , description = content , topic = topic)
            complaint.save()
            
            send_mail(subject,content ,EMAIL_HOST_USER,["bravelaboratory2023@gmail.com"],html_message=html)
            
            return redirect('client')
        
    else:
        form = ComplaintForm()

    context = {
        'form': form
    }
    return render(request, 'client/complaint/complaint.html', context)
    