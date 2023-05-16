from django.shortcuts import render ,redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required , permission_required
from django.template.loader import render_to_string
from brave_lab_project.settings import EMAIL_HOST_USER
from .forms import ClientContactForm, ComplaintForm

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
    
    return render(request,'client/appointment/appointment_book.html')

@login_required
@permission_required('client.view_client', raise_exception=True)
def appointment_confirm(request):
    
    return render(request,'client/appointment/appointment_confirm.html')

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
    