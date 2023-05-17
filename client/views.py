from datetime import datetime
from decimal import Decimal
from django.shortcuts import render ,redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required , permission_required
from django.template.loader import render_to_string
from brave_lab_project.settings import EMAIL_HOST_USER
from main_home.models import Appointment, MedicalDocument, TestOffered
from .forms import  AppointmentForm, AppointmentPaymentForm, ClientContactForm, ComplaintForm
from django.core.files.storage import default_storage

# Create your views here.

################################################################

# Home

@login_required
@permission_required('client.view_client', raise_exception=True)
def client_home(request):
    
    return render(request,'client/client.html')

################################################################

# Appointment

@login_required
@permission_required('client.view_client', raise_exception=True)
def appointment_book(request):
        
    form = AppointmentForm()   
         
    return render(request,'client/appointment/appointment_book.html',{'form':form})

@login_required
@permission_required('client.view_client', raise_exception=True)
def appointment_confirm(request):
    
    if request.method == 'POST':
        
        if request.POST.get("date") :
            
            form = AppointmentForm(request.POST,request.FILES)
            
            if form.is_valid():
                
                date = form.cleaned_data['date']
                date = date.strftime("%Y-%m-%d")
                description = form.cleaned_data['description']
                tests_requested = form.cleaned_data['tests_requested']
                
                document_file = request.FILES['document']
                document = default_storage.save('medical_documents/' + document_file.name, document_file)
                
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
            
        elif request.POST.get("payment_option") :
            
            form = AppointmentPaymentForm(request.POST)
            
            if form.is_valid:
                client = request.user.client
                payment_option = request.POST.get('payment_option')
                
                tests_requested=[]
                test_count = int(request.POST.get("data.test_count"))
                for i in range(1,test_count+1):
                    test_id = int(request.POST.get(f"data.tests_requested{i}"))
                    test = TestOffered.objects.get(id=test_id)
                    tests_requested.append(test)
                    
                date = datetime.strptime(request.POST.get("data.date"), "%Y-%m-%d").date()
                description = request.POST.get('data.description')
                document = request.POST.get('data.document')
                total_price = Decimal(request.POST.get('data.total_price'))
                
                appointment = Appointment()
                appointment.client = client
                appointment.date = date
                appointment.description = description
                appointment.document = document
                appointment.total_price = total_price
                appointment.payment_option = payment_option
                appointment.save()

                # Add the tests_requested to the appointment
                appointment.tests_requested.add(*tests_requested)
                
                
                return redirect('client')
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
def appointment_detail(request):
    
    return render(request,'client/appointment/appointment_detail.html')

################################################################

# Request

@login_required
@permission_required('client.view_client', raise_exception=True)
def request_list(request):
    
    return render(request,'client/request/request_list.html')

@login_required
@permission_required('client.view_client', raise_exception=True)
def request_detail(request):
    
    return render(request,'client/request/request_detail.html')

################################################################

# Result

@login_required
@permission_required('client.view_client', raise_exception=True)
def result_list(request):
    
    return render(request,'client/result/result_list.html')

@login_required
@permission_required('client.view_client', raise_exception=True)
def result_detail(request):
    
    return render(request,'client/result/result_detail.html')

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
            
            send_mail(subject,content ,EMAIL_HOST_USER,["bravelaboratory2023@gmail.com"],html_message=html)
            
            return redirect('client')
        
    else:
        form = ComplaintForm()

    context = {
        'form': form
    }
    return render(request, 'client/complaint/complaint.html', context)
    